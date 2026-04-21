# Project Overview

This project aims to transform an academic cryptography project into a production-ready system.

The original version was a Java desktop application that allowed users to send encrypted email attachments using an Identity-Based Encryption (IBE) scheme. It relied on the JPBC library for pairing-based cryptography.

This new version focuses on re-implementing the system with modern tools while studying the real-world challenges of deploying cryptographic systems in production environments.

## Objectives

Study real-world constraints, including:

- Key management

- Security hardening

- Deployment architecture

- Scalability

- Technical Stack

# Current Status

A first python version is implemented with charm crypto. It reproduces  the academic logic of IBE from Boneh-Franklin.
A second rust version is being implemented with arkworks. For that version, i am using the CL-IBE from Al Riyami and Paterson paper. It eliminates the key-escrow problem and arkworks provides curves for production-ready application. Here is the code repository https://github.com/Khady71/certificatless-ibe-on-arkworks.



# Future Work

- Define a production-ready key management architecture

- Specify a threat model

- Explore secure deployment strategies

# Build in Public

The development process and technical decisions are documented publicly on LinkedIn:

https://www.linkedin.com/in/khady-gaye
