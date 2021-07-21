cd ..
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -f LeakDetection/Dockerfile -t wagonorge/va-leak-detection --push .