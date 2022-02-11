Selective Region Hybrid Multiple Key Authentication System for Digital Image

Abstract 

Security is a very important concern in the 20th century. Pictures and multimedia data have become a common part of our life, it is very important that they are encrypted and safely secured and visible only to those who have the authority to view the data . At the same time it can be noticed that all parts of the image are not sensitive, and hence does not benefit from encryption.Our project aims to overcome this extra computations by detecting the sensitive parts of the image(faces) by using Computer Vision models and encrypting only that section of the image. We also propose a hybrid encryption algorithm that uses a two step encryption mechanism to enhance the overall security. In our proposed method we first perform symmetric encryption of the  image with a user-defined key using CBC followed by an asymmetric encryption performed by the RSA algorithm. These two algorithms synergise to provide a robust and secure encryption technique that performs better than existing techniques.
Motivation.In this day and age, where pictures and multimedia data have become a common part of our life, it is very important that they are encrypted and safely secured and visible only to those who have the authority to view the data. At the same time it can be observed that not all parts of the picture are sensitive. Thus, it is redundant and can be considered a waste of resources to encrypt the whole image.

Aim

In our project we aim to identify the sensitive parts of an image through computer vision models like OpenCV and only encrypt them(Eg: faces of people are considered as sensitive information). For this project we propose a hybrid image encryption algorithm that outperforms existing algorithms in terms of security.

Methodology

To show proof of concept, in this project we will be considering people captured in CCTV footage. The faces of these people can be considered as sensitive and private data, and hence, ought to be encrypted. Traditionally, the whole picture is encrypted and stored in the database.In our proposed method we will be using Computer Vision models like OpenCV to detect and isolate the face. Once the face is detected,we will use our encryption algorithm to encrypt only the bounded box. This way we would encrypt only the sensitive data, and would save unwanted computations. It is important to note that once the face is detected and encrypted, the 4 corners of the bounded box must be stored in the image as encrypted data. These 4 corners will be very important for the decryption of the face, as it will give us the location to start the decryption. We will also be proposing a hybrid encryption image encryption algorithm to increase the security and robustness of the image.

Proposed Methodology:

The first step involves the detection of the sensitive parts of the image through the computer vision model OpenCV. We make a Rectangular outline around each sensitive part by using a bounded box. The four corners of the bounded box are stored and the image inside the bounded box region is inputted into our hybrid algorithm. 

Any image encryption algorithm has two basic steps:

Diffusion: Changing the values of the pixels (R, G, B).

Scrambling: Swapping and changing the original position of the pixels.

With the combination of these two techniques an image can be encrypted. The strength of the encryption highly depends on the randomness of the scrambling and diffusion.
 
The image encryption algorithm that we are proposing will be a combination of symmetric as well as asymmetric encryption. We will be taking a key as input from the user and performing scrambling and diffusion based on this key. We will also be performing asymmetric encryption by making use of the RSA algorithm. Thus the RSA algorithm will provide the user with the private key after the encryption. 

PBKDF2 Hashing: We will take the key from the user and obtain an expanded hash value, by using a key extension algorithm (PBKDF2). This algorithm is used to strengthen passwords, in our case it is used to increase the size of the key, so that its length is equal to our pixel count. This way we protect our image encryption from having a very weak key that can be decoded very easily. The values obtained from PBKDF2 are unique and will further enhance the security of the algorithm. The obtained hash value is then split into an array of  N elements ranging from 0 to 256. The number of elements(N) in this array is equal to the number of pixels in the image. To further increase the randomness we add the values of 5 consecutive key values in the key array and perform modulus 256 to get the final list of key values.





Cipher Block Chaining(XOR): CBC is a very well known method and is recognised for providing message confidentiality. It is the advanced version of ECB which compromises security requirements because of the direct relationship between the original image and the key.In our algorithm we will be using the Cipher Block Chaining method to perform the diffusion on the pixels. In this method we traverse each pixel and encrypt it by performing XOR operation on each pixel with the key array as well the previous encrypted  pixel.By XORing with the previous encrypted pixel before being encrypted with the key,it greatly increases the variation in the encrypted values.Thus pixels with similar r,g,b values will not have the same encrypted value,thereby making our algorithm more secure and less predictable.


Scrambling: In this step we perform row and column rotation on the pixels obtained from the previous step. The main aim of this step is to increase the entropy of the pixels. The pixels cannot remain close to their original position. In our algorithm we perform row rotation of pixels followed by column rotation of the pixels. This set of operations is performed 2 times to get the optimum scrambling. The rotation is based on the modulus of the key value obtained from the hash array. Thus the scrambling is unique to each key and provides added security.We alternate the direction of rotation based on the row and column number to further increase the randomness. This is a simple yet very powerful step that makes the algorithm more secure. It changes the location of the pixels making it harder to decrypt with the wrong key. Thus by effectively scrambling the pixels all across the image, we can recover most of the original image even if a part of it is lost. 

RSA: RSA algorithm is an asymmetric encryption technique  and its strength is based on the tremendous difficulty of factorising two large Pseudo Random Prime numbers generated during encryption.Therefore greater the key length,the longer it takes to crack the prime numbers thereby increasing the security. RSA is good for plain text,but not very effective for images as the picture may retain its visual feature after encryption. In the RSA algorithm pixels with the same value obtain the same encrypted value, and since we are using an image, the similarity of the pixels can be clearly identified. In our algorithm we perform RSA in the last step when the image has no recognizable feature because of the 2 precursor steps. Thus we overcome this drawback of RSA while adding an extra layer of security to our proposed algorithm. After encryption we provide the user with the public as well as the private key used for the encryption.The advantage of RSA is that even if the user guesses a number close to the original key, the obtained decrypted image is not recognisable. The original key alone can decrypt the original image,no other key can give the decrypted image and cracking of the original key is very time consuming and next to impossible when the key length is very large.
Thus our proposed system will have a Multistep Key Authentication during image decryption. The user will have to enter the Original Key (User Generated) as well as the RSA Key (System Generated) provided at time of decryption. Thus even if one of the keys is compromised, the original image will not be retrievable. By incorporating traditional XOR operation with the RSA algorithm we have come up with an effective hybrid algorithm that is very secure.
