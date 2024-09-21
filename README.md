# Agumented-Reality-in-Disguise-ARID-

## Overview
The Brilliant Monocle project is an innovative application that utilizes augmented reality (AR) technology to scan QR codes and retrieve hidden messages. Users can capture images using the monocle's camera, which then analyzes the photo for QR codes. If a QR code is detected, the associated text is displayed on the screen, and the user has the option to search for a hidden message linked to their user ID.

### How It Works
1. **Image Capture**: The user takes a photo with the monocle by pressing a button.
2. **QR Code Detection**: The software scans the image for QR codes. If no QR code is found, an error message appears on the display.
3. **Display of Found Text**: If a QR code is found, its text is displayed, and the user can initiate a search for a hidden message.
4. **Server Query**: When prompted, the application sends a request to the server using the QR code and the user ID. If a hidden message exists, it will be shown on the display. If no message is found, the user can leave a new message, which will be sent to the server for confirmation.

### Software Architecture
The main sequence of our software has been extensively analyzed using activity diagrams. The physical distribution of the software is highlighted in the distribution diagram (see Figure 1.2). The application primarily runs on the client side, structured into two subcomponents: **Encryption** and **Machine Vision**. The monocle serves as the primary input/output interface between the user and the application, as well as between images and messages. The database functions as an essential extension for communication purposes.

For future porting to more powerful hardware, the model can be easily adapted to operate on both client devices and servers. Currently, a Bluetooth Low Energy (BLE) connection is still required for functionality.

## Features
- **QR Code Scanning**: Detects and decodes QR codes in real-time.
- **Hidden Message Retrieval**: Displays messages linked to scanned QR codes.
- **User Interaction**: Allows users to leave messages if no hidden message is found.

## Installation
To get started with the project, clone the repository and install the required dependencies.

```bash
git clone https://github.com/pastaLavista5/Agumented-Reality-in-Disguise-ARID-.git
cd Agumented-Reality-in-Disguise-ARID-
