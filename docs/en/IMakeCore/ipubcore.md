# IPubCore Package Distribution Website

> This document describes how to use IPubCore.

The IPubCore website is a platform provided by IMakeCore for searching and downloading packages. The website address is [https://pub.iwebcore.org](https://pub.iwebcore.org).

IPubCore is built with the backend using IHttpCore from the IHttpCore framework in IWebCore, and the frontend is developed with React. It is recommended that users use IHttpCore to create their own HTTP server.

Users can search for various packages on this website. Once a package is found, the package name and version can be added to the `packages.json` file. IMakeCore will automatically download the package and integrate the specified version.

The interface of the IPubCore website is shown below:

![image-20250713162242016](assets/image-20250713162242016.png)

## How to Find and Use Packages

Users can search for packages by entering keywords on the [search page](https://pub.iwebcore.org/search.html). Clicking on a found package will display its detailed information.

## How to Register and Login

Users can register and log in by clicking the [Login](https://pub.iwebcore.org/login.html) / [Register](https://pub.iwebcore.org/register.html) button in the top-right corner of the website.

## How to Publish Packages

### Email Verification

To publish a package, users must complete email verification.

Due to website configuration, users cannot upload packages by default. They need to contact the administrator to request approval. The administrator will review the request and grant the appropriate permissions. To contact the administrator, users should send an email to the [administrator email](mailto:yuekeyuan001@gmail.com) using the registered email address for confirmation.

When sending an email, users must include the following content:

```
I want to publish a package, so I send this email.
I send this email to indicate my intention to publish packages.
```

Unfortunately, I'm currently very busy and cannot resolve this feature quickly. (This feature is missing but the adjustment required is small. However, I'm simultaneously working on the entire system and also job-seeking, so my time is very limited.)

### Packaging

Currently, users need to manually package their packages. In the future, packaging and uploading will be handled by the `ipc` tool.

Users can package the project's standalone package directly into a `.zip` file using a zip tool. Note that during packaging, the `package.json` file must be placed in the root directory of the zip file and cannot be nested in a subdirectory.

For guidance on how to define a package, please refer to the [Defining Packages](./definePackage.md) documentation.

### Publishing Packages

After logging in, users can click on their username in the top-right corner and select the `My Package` option from the dropdown menu, which will redirect them to the [Package Management](https://pub.iwebcore.org/packagemanage.html) page. On this page, users can click the "Upload Package" button to access the [Package Upload](https://pub.iwebcore.org/packageupload.html) page. Here, users can drag and drop the pre-packaged package to complete the upload.

Before publishing a package, users must verify their email address.

During the upload process, the package information will be validated. If the validation fails, users should modify the package according to the feedback provided.