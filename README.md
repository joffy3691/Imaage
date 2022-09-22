# Selective-Region-Hybrid-Multiple-Key-Authentication-System-for-Digital-Image

Security is a very important concern in the 20th century. Pictures and multimedia data have become a common part of our life and it is very important that they are encrypted, safely secured and visible only to those who have the authority to view the data . At the same time it can be noticed that every part of the image is not sensitive, and hence does not benefit from encryption. Our project aims to overcome these extra computations by detecting the sensitive parts of the image (faces, in our case) by using Computer Vision models and encrypting only that section of the image. We also propose a hybrid encryption algorithm that uses a two step encryption mechanism to enhance the overall security. In our proposed method we first perform symmetric encryption of the  image with a user-defined key using CBC, followed by an asymmetric encryption performed by the RSA algorithm. These two algorithms synergise to provide a robust and secure encryption technique that performs better than existing techniques.
## Screenshots

**Overall Architecture**
![Overall Architecture](/architecture.png)

**Encryption Process**
![Overall Architecture](/enc.png)

**Decryption Process**
![Overall Architecture](/dec.png)
