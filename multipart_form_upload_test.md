# Performance evaluation of uploading multiple gigabytes of data using multipart/form-data POST HTTP request.

Using nginx as server and several Python2 http libraries as clients.

Client:
- poster
    - 38MB/s (single cpu thread 100% load)
    - 240 MB/s (modified poster, increase blocksize to 8MB, comment out regex)
    - 384 MB/s (same as before, blocksize increased to 64MBs, using larger 6GB file)
- requests_toolbelt
  - 200MB/s (increased blocksize in used httplib to 8MB)
- sockets (my own implementation without using an HTTP lib):
  - 425MB/s
  - 590MB/s (using fake data stream, no access to SATA6 SSD)
  - 600MB/s using TCP_NODELAY=1. This is the limit of the Windows loopback adapter. Using Linux/Debian speed is twice as fast.
- I also tried some other http libraries but they were even slower. The common problem is that the upload chunks are super small which is ok for normal forms but not for uploading files with multiple gigabytes in size.