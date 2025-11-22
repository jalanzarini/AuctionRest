#!/bin/zsh

echo "Starting APIGateway.py in the background..."
alacritty --working-directory ~/Faculdade/SistDist/AuctionRest/backend/ -e uv run gunicorn 'APIGateway:run()' &

echo "Starting MSLeilao.py in the background..."
alacritty --working-directory ~/Faculdade/SistDist/AuctionRest/backend/ -e uv run MSLeilao.py &

echo "Starting MSLance.py in the background..."
alacritty --working-directory ~/Faculdade/SistDist/AuctionRest/backend/ -e uv run MSLance.py &

echo "Starting MSPagamento.py in the background..."
alacritty --working-directory ~/Faculdade/SistDist/AuctionRest/backend/ -e uv run MSPagamento.py &

echo "Starting MockPayment.py in the background..."
alacritty --working-directory ~/Faculdade/SistDist/AuctionRest/backend/ -e uv run MockPayment.py &

# Wait for all background jobs to complete before exiting the script
#wait

#echo "All background scripts finished."
