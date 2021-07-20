from opcua import Client, ua, Node
import paho.mqtt.client as mqtt
from threading import Thread, Lock
from dotenv import load_dotenv
from OPCUA_MQTT_link.utils import (
    getTagname,
    getNewHash,
    setTimestamp,
)
import time
import datetime
import json
import os
import logging
import copy



def buildNodeTree(pObject, nodeStore, OpcNodes):
    for node in OpcNodes:
        children = node.get_children()
        tagname = getTagname(node)
        if len(children) == 0:
            if tagname.startswith("_"):
                pObject[tagname] = node.get_value()
            else:
                nodeStore[tagname] = node
                pObject[tagname] = node.get_value()
        else:
            nodeStore[tagname] = {}
            pObject[tagname] = {}
            buildNodeTree(pObject[tagname], nodeStore[tagname], children)


def getValuesFromNodes(pObject, nodeStore):
    for tagname, pObje in pObject.items():
        if tagname.startswith("_"):
            continue
        if type(pObje) is dict:
            getValuesFromNodes(pObje, nodeStore[tagname])
        else:
            pObject[tagname] = nodeStore[tagname].get_value()


def setValuesToNodes(pObject, nodeStore):
    for tagname, pObje in pObject.items():
        if tagname.startswith("_"):
            continue
        if type(pObje) is dict:
            setValuesToNodes(pObje, nodeStore[tagname])
        else:
            value = pObje
            node = nodeStore[tagname]
            if type(value) is str:
                node.set_value(value)
            elif type(value) is bool:
                node.set_value(value)
            elif type(value) is float:
                node.set_value(value, varianttype=ua.VariantType.Float)
            elif type(value) is int:
                node.set_value(value, varianttype=ua.VariantType.Int16)
            else:
                raise Exception("PLC: Type not found")


def on_mqtt_connect(client, userdata, flags, rc):
    logging.info("PLC: MQTT Connected with result code " + str(rc))
    client.subscribe(mqttTopicSubscribeData)


def on_mqtt_disconnect(client, userdata, rc):
    logging.exception("PLC: MQTT disconnecting: " + str(userdata) + ", " + str(rc))


def on_received_mqtt_message(client, userdata, msg):
    global hashsLock, hashs, nodes, tags
    receivedObject = json.loads(str(msg.payload, encoding="utf-8"))
    # If plc receive empty objects, it send an object with values in return, immediately
    tagname = receivedObject["_tagId"]
    if receivedObject["_type"] == "":
        logging.warning("PLC: HMI is missing data and requesting: " + tagname)
        pObject = tags[tagname]
        getValuesFromNodes(pObject, nodes[tagname])
        newHash = getNewHash(pObject)
        setTimestamp(pObject)
        # Publish and save hash
        mqttClient.publish(mqttTopicPublishData, payload=json.dumps(pObject))
        with hashsLock:
            hashs[tagname] = newHash
        return

    # Generate new hash
    logging.warning("PLC: HMI is sending CMD: " + tagname)
    newHash = getNewHash(receivedObject)
    # Store hash
    with hashsLock:  # Sending data only on change, therefor no need to check for change
        hashs[receivedObject["_tagId"]] = newHash
    # Write to opc ua by setting the children recursive
    setValuesToNodes(receivedObject, nodes[tagname])


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.WARNING,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.warning("PLC: Starting OPC-UA - MQTT link")
    load_dotenv()
    # Global variables
    tags = {}
    nodes = {}
    hashs = {}  # Storing a hash of the object to be able to compare two objects fast
    hashsLock = Lock()  # hashs are used in multiple threads
    publishLoopWaitTime = int(os.getenv("WAIT_TIME"))  # For testing
    ## Opc UA
    opcUaServer = os.getenv("OPC_UA_SERVER")  # Host of opcua server
    opcUaServerUsername = os.getenv("OPC_UA_SERVER_USERNAME")
    opcUaServerPassword = os.getenv("OPC_UA_SERVER_PASSWORD")

    #Collectiong and generating first part of nodeID string
    opcUaId = os.getenv("OPC_UA_ID")
    opcUaPls = os.getenv("OPC_UA_PLC")
    opcUaIdStart = "ns=4;s=|var|" + opcUaId + "." + opcUaPls #Contains the start of the node adress. Continue with "." to navigate nodes

    #Generates the rest of the node strings
    opcUaIdHMI = opcUaIdStart + ".HMI"
    opcUaIdCounter = opcUaIdStart + ".STATUS.OpcUaMqttLinkStatus.AliveCounterPv"
    opcUaIdLastRun = opcUaIdStart + ".STATUS.OpcUaMqttLinkStatus.LastRun"
    opcUaIdRestartCmd = opcUaIdStart + ".STATUS.OpcUaMqttLinkStatus.Restart_Cmd"
    ## MQTT
    mqttBroker = os.getenv("MQTT_BROKER")
    mqttPort = int(os.getenv("MQTT_PORT"))
    mqttTopicPublishData = os.getenv("MQTT_TOPIC_PUBLISHDATA")
    mqttTopicSubscribeData = os.getenv("MQTT_TOPIC_SUBSCRIBEDATA")
    mqttPublishPvSuffix = os.getenv(
        "MQTT_PUBLISH_PV_SUFFIX"
    )  # Published every sample, other tags are pulished on data change
    logging.warning(
        "PLC: Prepared with this: OpcUaServer: "
        + opcUaServer
        + ", OpcUaIdHMI"
        + opcUaIdHMI
        + ", MqttBroker: "
        + mqttBroker
    )
    # OPC UA
    opcClient = Client("opc.tcp://" + opcUaServer + ":4840", timeout=3)
    opcClient.set_user(opcUaServerUsername)
    opcClient.set_password(opcUaServerPassword)

    # MQTT
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_mqtt_connect
    mqttClient.on_disconnect = on_mqtt_disconnect
    mqttClient.on_message = on_received_mqtt_message
    # Ensure disconnecting on program close
    try:
        # Tries to reconnect every 10 seconds
        logging.warning("PLC: Waiting 10s for e!cockpit to start")
        time.sleep(10)
        while True:
            try:
                logging.warning("OPCUA: Connecting to Opc...")
                opcClient.connect()
                if opcClient is None:
                    raise Exception("OPCUA: Opc connection failed")
                logging.warning("OPCUA: OPC Connected!")


                # Building tag and opc node trees, for better performance on publishing data
                nodesUnderPrefix = opcClient.get_node(opcUaIdHMI)
                logging.warning("OPCUA: Getting children: " + opcUaIdHMI)
                topLevelOpcNodes = nodesUnderPrefix.get_children()
                logging.warning("OPCUA: number of nodes in HMI: " + str(len(topLevelOpcNodes)))

                logging.warning("OPCUA: building node tree")
                if len(topLevelOpcNodes) == 0:
                    raise Exception("OPCUA: No tags where found")
                for topLevelOpcNode in topLevelOpcNodes:
                    tagname = getTagname(topLevelOpcNode)
                    tags[tagname] = {}
                    tags[tagname]["_timestamp"] = {}
                    nodes[tagname] = {}
                    buildNodeTree(tags[tagname], nodes[tagname], topLevelOpcNode.get_children())


                logging.warning("MQTT: Connecting to MQTT broker...")
                mqttClient.connect(mqttBroker, mqttPort, 60)
                mqttThread = Thread(target=mqttClient.loop_forever, args=())
                mqttThread.start()
                logging.warning("MQTT: Waiting 2s...")
                time.sleep(2)  # MQTT need time to connect

                loopCounter = 0
                # Read data from OPC UA and Publish data to MQTT loop
                while True:
                    publishLoopStarttime = time.time()
                    loopCounter = loopCounter + 1
                    # OPC UA Nodes are at start -> need for restart if there are new nodes
                    for tagname, pObject in tags.items():
                        # Building python object, then converting to json before sending
                        getValuesFromNodes(pObject, nodes[tagname])
                        # Publishing
                        if mqttPublishPvSuffix in tagname:
                            setTimestamp(pObject)
                            mqttClient.publish(mqttTopicPublishData, payload=json.dumps(pObject))
                        else:
                            newHash = getNewHash(pObject)
                            setTimestamp(pObject)
                            if tagname in hashs:
                                if hashs[tagname] != newHash:
                                    # Publish and save hash
                                    mqttClient.publish(
                                        mqttTopicPublishData, payload=json.dumps(pObject)
                                    )
                                    with hashsLock:  # Threadsafe
                                        hashs[tagname] = newHash
                            else:
                                # Publish
                                mqttClient.publish(
                                    mqttTopicPublishData, payload=json.dumps(pObject)
                                )
                                # Tagname does not exist in hashs
                                # Save hash
                                with hashsLock:  # Threadsafe
                                    hashs[tagname] = newHash
                    logging.warning(
                        "MQTT: publish loop used [s]: " + str((time.time() - publishLoopStarttime))
                    )


                    node = opcClient.get_node(opcUaIdCounter)
                    node.set_value(loopCounter, varianttype=ua.VariantType.Int16)
                    node = opcClient.get_node(opcUaIdLastRun)
                    node.set_value(time.ctime())

                    restartCmdNode = opcClient.get_node(
                        opcUaIdRestartCmd
                    )
                    if restartCmdNode.get_value():
                        restartCmdNode.set_value(False)
                        raise Exception("PLC: Restart demanded from e!Cockpit environment")

                    time.sleep(publishLoopWaitTime)
            except Exception:
                logging.exception("PLC: Exception in connection loop.")
            finally:
                logging.warning("PLC: Disconnecting, then reconnecting after 10s.")
                time.sleep(10)
                try:
                    if opcClient is not None:
                        opcClient.disconnect()
                except:
                    logging.exception("PLC: Exception when trying to disconnect OPC")
                try:
                    mqttClient.disconnect()
                except:
                    logging.exception("PLC: Exception when trying to disconnect MQTT")
    except:
        logging.exception("PLC: Exception in main.")
    finally:
        logging.warning("PLC: OPC UA - MQTT link is shutting down.")
