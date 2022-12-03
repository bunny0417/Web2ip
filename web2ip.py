import argparse
import socket
from threading import Thread

def resolve_hostname(website, results):
  try:
    # Attempt to resolve the hostname to an IP address
    ip_address = socket.gethostbyname(website)
    results.append(ip_address)
  except socket.gaierror as e:
    # If the hostname could not be resolved, print an error message
    if e.errno == socket.EAI_NONAME:
      print(f'Error: Host "{website}" not found')

def main():
  # Create the argument parser
  parser = argparse.ArgumentParser(description='Convert a list of websites to IP addresses')
  parser.add_argument('-d', '--file', type=argparse.FileType('r'), help='The file containing the list of websites')
  parser.add_argument('-u', '--url', help='A single website to be resolved')

  # Parse the command line arguments
  args = parser.parse_args()

  # If a file was specified, read the list of websites from it
  if args.file:
    websites = args.file.read().splitlines()
  else:
    websites = [args.url]

  # Create a list to store the results
  results = []

  # Create a thread for each website
  threads = [Thread(target=resolve_hostname, args=(website, results)) for website in websites]

  # Start the threads
  for thread in threads:
    thread.start()

  # Wait for the threads to finish
  for thread in threads:
    thread.join()

  # Print the results
  for ip_address in results:
    print(ip_address)

if __name__ == '__main__':
  main()
