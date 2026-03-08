# configs.json  
> This document describes the configuration items in the configs.json file.  

## Overview  

The configs.json file stores system configuration information for IMakeCore.  

Users should not modify this content easily.  

---

## Configuration Items  

### globalLibStore  

The `localLibStore` field defined in packages.json represents the current `system package` location. This field corresponds to a string that specifies a folder path. The field can be omitted; if omitted, the default path is the `.lib` folder under the IMakeCore system path. Users can define the globalLibStore path themselves.  

Packages requested over the network will be installed in this location.  

---

### libStores  

The value of the `libStores` field is an array that represents a list of folders for storing packages. The `libStores` field can be omitted by default, resulting in an empty list.  

**Note**: The `libStores` defined in the project's packages.json takes precedence over the `libStores` defined in IMakeCore's configs.json. When IMakeCore loads packages, if a package with the same name and version is found, it will prioritize loading from the project's libStore.  

The `libStores` defined in configs.json applies to all projects.  

If users have additional packages stored in different folders, they can add the corresponding folder paths to the `libStores` field. IMakeCore will then recognize and process these packages.  

---

### servers  

The value of the `servers` field is an array type, where strings can be stored. By default, it is an empty list, and the field can be omitted. The strings inside the `servers` field must be server paths. Users can provide multiple server addresses for downloading packages.  

For example, the following are valid paths:  

```txt
http://127.0.0.1:8000
https://abc.com
http://abc.com:81
```  

**Note**: The paths here must be `scheme + host` paths and cannot include path information. The following paths are invalid:  

```txt
http://127.0.0.1/
http://abc.com/hello
```  

The purpose of `servers` is to provide network-based package services. IMakeCore can query and download packages from the corresponding servers.  

Servers defined earlier in the `servers` field take precedence over those defined later. The `servers` defined in packages.json take precedence over those in the IMakeCore system configuration. During package queries and downloads, IMakeCore will call server addresses in order of priority. If a server cannot fulfill the request (e.g., connection issues or the package is unavailable), IMakeCore will proceed to the next server in the list.  

---

### user  

The `user` field contains the username provided by the user when registering on the IPubCore website.  

This field is only used for package uploads via the `ipc` tool and will not be used for other purposes (collecting user information). *(Currently, due to the incomplete `ipc` package upload functionality, this field will not be used).*  

Users can view their username using the `ipc user` command and set it using the `ipc user set` command.  

---

### email  

The `email` field contains the email provided by the user when registering on the IPubCore website.  

This field is only used for package uploads via the `ipc` tool and will not be used for other purposes (collecting user information). *(Currently, due to the incomplete `ipc` package upload functionality, this field will not be used).*  

Users can view their email using the `ipc email` command and set it using the `ipc email set` command.