# Practical Work 1

- **System architecture**

The project built in Python with the help of the PyCharm IDE was structured with basically three main files. These files were responsible, respectively, for the operation of the server, for the client's interaction and for structuring the LRU cache class.

- **Technologies**

The main libraries used were the socket and thread libraries, both native to Python.

Socket programming is a way of connecting two nodes on a network to communicate with each other. One socket/node listens on a particular port at an IP, while the other socket reaches out to the other to form a connection. In this project the server forms the listener socket while all the clients can reaches out to the server.

To deal with the possibily of multiple clients connecting to the server the thread functionaly comes handy. Thread is a way in which a process/task of a computer program is divided into two or more tasks that can be executed concurrently. And, as mentioned before, threads are used to let many clients access the functions offered by the server.

- **Protocols**

A basic server-client TCP connection was made using the socket Python library. The TCP, or Transmission Control Protocol, is one of the communication protocols, of the transport layer of the computer network of the OSI Model, which support the global Internet network, verifying that data is sent in the correct sequence and without errors via the network.

- **Project decisions**

One of the most important project decisions was to choose the Least Recently Used structure to be the foundation to the cache. This choice happened because the LRU data structure perfectly fits the interaction expected by a cache.

> A Least Recently Used (LRU) Cache organizes items in order of use, allowing you to quickly identify which item hasn't been used for the longest amount of time.
Picture a clothes rack, where clothes are always hung up on one side. To find the least-recently used item, look at the item on the other end of the rack. <em>Source: <https://www.interviewcake.com/concept/java/lru-cache></em>

This way the LRU cache will always keep the most frequently accessed files in the first positions of the cache and whenever a deletion needs to be performed in the cache, the last item will be removed, as it is the least frequently accessed.

In the project developed, the implementation of the LRU cache is, in essence, identical to that represented by Figure 1. The only differences are in the use of a Python dictionary instead of the hash map and the presence of nodes instead of articles in each item of the linked list. In Figure 1, it is possible to observe the role of the hash map in changing the positions of items when necessary.

### Figure 1:

<img src="https://files.realpython.com/media/cache_internal_representation_1.6fdd3a39fa28.png" width="400" height="400"/>

<em>Source: <https://realpython.com/lru-cache-python/></em>

Each of the nodes present in the dictionary has a key, content, value and lock attribute. The key attribute contains the name of the file stored at that position, the content contains the text present in the file, the value represents the size of the file stored at that position and the lock attribute is a boolean variable activated only when a node removal is started.

- **Mutual exclusion solution**

Mutual exclusion is the property of a program that guarantees that only one process has access to a given shared variable at any one time. It is the simplest solution to obtain the non-deterministic semantics of a parallel program.

As an initiative to implement mutual exclusion, a lock attribute was thought to alert the system when a file is passing through deletion in the cache, in this way no process will be able to consult or change a file being deleted from the cache, these actions could lead to inconsistency of the cache.

- **Extras**

The video of the project's operation can be found at this [link](https://youtu.be/aanUUhS2w5M).
