# Security Policy

Thank you for your interest in the security of **SPROCTOR**! We take security very seriously and appreciate any contributions to keep our project safe and reliable. This document outlines how to report vulnerabilities, our supported versions, and best practices to follow when contributing to or using SPROCTOR.

---

## Supported Versions

We provide security updates for the following versions of SPROCTOR. Please upgrade to one of these versions to ensure continued protection:

| Version        | Supported           |
| -------------- | ------------------- |
| Latest (1.x)   | ✔️                  |
| Previous (0.x) | ❌                  |
| **Node.js**    | **Version 14** ✔️   |
| **Python**     | **Version 3.12** ✔️ |

---

## Reporting a Vulnerability

If you discover a security vulnerability in SPROCTOR, please follow these steps:

1. **Contact Us Privately**  
   Report security issues **privately** by emailing our security team at [security@sproctor.com](mailto:security@sproctor.com). This allows us to investigate and resolve the issue before public disclosure.

2. **Provide Details**  
   Include detailed information to help us understand and replicate the issue, such as:

   - Affected version(s)
   - Steps to reproduce the vulnerability
   - Potential impact of the issue
   - Suggested solutions, if any

3. **Wait for Our Response**  
   We aim to respond to security reports within **48 hours**. If we validate the vulnerability, we will work on a fix and keep you updated.

---

## Security Patch Process

1. **Validation and Confirmation**  
   After a report is received, our team will work to confirm and assess its severity. If valid, the vulnerability will be prioritized based on the impact level.

2. **Patch Development**  
   Our developers will create and thoroughly test a patch to resolve the issue. We ensure that security patches do not introduce new issues and adhere to best practices.

3. **Patch Release**  
   Once tested, the patch will be released as a part of a new minor or patch version update. Critical fixes may be released as hotfixes for immediate protection.

4. **Public Disclosure**  
   After a fix has been implemented, we will publicly disclose the vulnerability details in our [Changelog](https://github.com/tanishaness/SPROCTOR/blob/main/CHANGELOG.md) or a dedicated security advisory. Proper credit will be given to reporters unless they request anonymity.

---

## Best Security Practices for Contributors

We encourage all contributors to adhere to secure coding practices to prevent vulnerabilities. Here are some general guidelines:

- **Use Parameterized Queries**  
  Avoid SQL injections by using parameterized queries and ORM methods.
- **Sanitize User Inputs**  
  Always validate and sanitize any user-provided data to prevent XSS or other injection attacks.
- **Access Controls**  
  Implement strict access controls, especially for sensitive operations or admin areas.
- **Error Handling**  
  Avoid revealing sensitive information through error messages. Use descriptive but secure error handling practices.
- **Dependencies**  
  Regularly update dependencies to the latest secure versions and avoid vulnerable packages.

---

## Common Vulnerability Types

Be vigilant of the following common vulnerabilities when contributing to or using SPROCTOR:

- **Injection Attacks** (e.g., SQL, XSS)
- **Broken Authentication and Session Management**
- **Sensitive Data Exposure**
- **Security Misconfigurations**
- **Cross-Site Scripting (XSS)**
- **Insecure Deserialization**

---

## Responsible Disclosure

SPROCTOR follows a responsible disclosure policy to ensure security vulnerabilities are addressed promptly and transparently. By reporting a vulnerability, you agree to give us a reasonable amount of time to resolve the issue before publicly disclosing it.

If you have any questions or concerns about our security practices or wish to inquire about any past disclosures, feel free to reach out to us.

---

Thank you for helping keep SPROCTOR safe and secure!
