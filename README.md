# 🛹 XSMALI
A language transpilable from&to SMALI, made for easier reengineering Android APK-s.

[Before contributing, please read the last section.](#-in-case-of-the-project-getting-archived)

## 🤔 Why not Java
1. **⚠️ Avoiding problems:** There weren't many projects to transpile SMALI to Java, so I decided to make my own custom transpiler, as it's easiest to fix bugs in - my own software.

2. **⏳ Time-consuming setup:** Setting up a Java project from an existing structure takes time, which I'd rather avoid, especially since I'm not a Java expert.

3. **⚡ Performance:** XSMALI builds very fast compared to Java, since it doesn't validate code - it should contain enough information to compile to SMALI without advanced alghoritms.

## 🐋 Why not SMALI
1. **💁‍♂️ Not noob-friendly:** Beginners can't understand SMALI without 67 thousand Google searches, which is understandable.

2. **〽️ Additional complexity:** Even senior programmers may struggle to edit SMALI code, as it looks ugly and adds another layer of complexity to the whole process.

## 🛑 In-case of the project getting archived
XSMALI has been tested on actual parts of real apps from the Play Store, so it should work with all SMALI files up to the version supported by the last XSMALI update.

If you have a suggestion or stumbled upon a bug, you can create an issue or a feature request.
- **Merging into XSMALI:** I may have a hard time accepting pull requests as I hate Git and merging pull requests includes Git in the process.
- **Maintaining a fork:** If I don't accept or even see it, you can make your own fork of the repository, where you implement your proposed changes.

The project is made in Python and it's strongly typed, so it should be easy to contribute - as far as you know Python and have experience in creating programming languages.
