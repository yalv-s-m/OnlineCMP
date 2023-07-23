import docker
import time

client = docker.from_env()

# Build image
client.images.build(path='.', tag='my-py-app')

# Create container
container = client.containers.create('my-py-app', stdin_open=True, tty=True)

# Start container
container.start()

# Wait for container to be ready
while container.status != 'running':
    time.sleep(1)
    container.reload()

# Attach to the container's stdin/stdout/stderr
socket = client.api.attach_socket(container.id, params={'stdin': 1, 'stream': 1, 'stdout': 1, 'stderr': 1})

# Perform input/output operations
socket.sendall(b'Hello, World!\n')
output = socket.recv(4096)
print(output.decode())

# Close the connection and stop the container
socket.close()
container.stop()
container.remove()
