#!/bin/bash
#uv run gunicorn 'APIGateway:run()' -k gevent --threads=2
#sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
#sudo docker compose up -d

echo "Starting MSLeilao.py in the background..."
alacritty --working-directory ./ -e uv run MSLeilao.py &

echo "Starting MSLance.py in the background..."
alacritty --working-directory ./ -e uv run MSLance.py &

echo "Starting MSPagamento.py in the background..."
alacritty --working-directory ./ -e uv run MSPagamento.py &

echo "Starting MockPayment.py in the background..."
alacritty --working-directory ./ -e uv run MockPayment.py &

# Wait for all background jobs to complete before exiting the script
#wait

#echo "All background scripts finished."
