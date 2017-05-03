# Encryptr

# Idea

The idea is to send secret messages through images using our web and iOS apps. It is commonly known that images are the most shared resources in today’s world. More than 200 million people over the world use Instagram stories daily and Snapchat sees more than a million snaps created daily. With such a dominating effect of pictures in our lifestyles and everything being in the public domain, we thought of sending more information through this medium than just the image. The sender can selectively send the secret messages to whoever he decides, thus creating an end to end encryption system.

# Working (about web app and iOS app)

# Web App

The web app allows users to to upload a photo and a text message to encrypt in that photo. An interesting exploration of this concept was that only .PNG files work with our code and that is because .PNG files follow lossless compression techniques, thereby saving all of our encrypted data.
Once the user uploads the .PNG file, the file is sent to the flask server where the file is encrypted using our encryption algorithm.
Then there is a web-view in which the user is shown the original and the encrypted images (both looking the same to the naked eye).
The image can then be decrypted by our decryption algorithm, which runs completely independently of the encryption algorithm. Hence the message returned from the decryption algorithm is what it figures out from the decoding the image itself.

# iOS Application

The iOS app is an extension of the web application which most importantly serves as providing a private key to verify the receiver’s identity and run the decryption algorithm on your server. The App has two ways to input a photo. It can either be inputted from the phone’s camera or using the photo gallery. Once the photo is selected you can write your secret message, who it is meant for and submit it to our server. The server encrypts the image with the message and stores it. Each app comes with a receiver view which is a collection of all photos. The receiver needs to simply select the photo that is meant for him and use “Touch id” confirm his/her identify. After this confirmation is sent to our server it decrypts the image and returns the string to the user and it is displayed as alert box. 

# Encryption Algorithm

We encrypt the secret message in the pixels of the image. Each image is made by multiple pixels, which comprises of R (red), G (green) and B(blue) components. Each of this can have a value between 0 and 255 and is stored in 8 bits. We use these bits to store our message. 
The first step is to convert the message into a bit stream, which we do by appending ASCII characters (in Bits) of the message characters. Each character of the input message is 8 bits and hence we need 8 least significant bits to encrypt the message. The algorithm then iterates over each pixel of the image and stores a character in three pixels (3 RGB sets, hence 9 Bit Packets with 9 least significant bits), with one bit of the character replacing the least significant bit of one of the RGB bits.
We also store the length of the message in the last pixel of the image. That’s 24 bits, and can store message lengths of upto 2 ^ 24 characters (if the image is big enough). The message length is converted into bits and it completely replaces the last pixel bits, with the length bits and leading 0’s. In the decryption algorithm, we first decode the length of the message from the last pixel, then we iterate for that length over the image, take “bit packets” and convert those bits into characters and hence retrieve the message. 
