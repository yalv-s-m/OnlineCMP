FROM gcc:9.4.0

WORKDIR /home

COPY main.cpp /home

ENTRYPOINT g++ /home/main.cpp -o /home/a.out && /home/a.out
