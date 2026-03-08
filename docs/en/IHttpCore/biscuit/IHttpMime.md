|
| ------------------------------------- | ---------------------------------------------- |
| TEXT_PLAIN                            | text/plain                                     |
| TEXT_PLAIN_UTF8                       | text/plain; charset=UTF-8                      |
| TEXT_HTML                             | text/html                                      |
| TEXT_HTML_UTF8                        | text/html; charset=UTF-8                       |
| TEXT_CALENDAR                         | text/calendar                                  |
| TEXT_CSS                              | text/css                                       |
| TEXT_DIRECTORY                        | text/directory                                 |
| TEXT_ENRICHED                         | text/enriched                                  |
| TEXT_PARITYFIC                        | text/parityfec                                 |
| TEXT_RICHTEXT                         | text/richtext                                  |
| TEXT_RTF                              | text/rtf                                       |
| TEXT_SGML                             | text/sgml                                      |
| TEXT_T140                             | text/t140                                      |
| TEXT_URI_LIST                         | text/uri-list                                  |
| TEXT_VND_CURL                         | text/vnd.curl                                  |
| TEXT_XML                              | text/xml                                       |
| IMAGE_MICROSOFT_ICO                   | image/vnd.microsoft.icon                       |
| IMAGE_JPEG                            | image/jpeg                                     |
| IMAGE_PNG                             | image/png                                      |
| IMAGE_TIFF                            | image/tiff                                     |
| IMAGE_SVG_XML                         | image/svg+xml                                  |
| IMAGE_BMP                             | image/bmp                                      |
| IMAGE_CGM                             | image/cgm                                      |
| IMAGE_G3FAX                           | image/g3fax                                    |
| IMAGE_GIF                             | image/gif                                      |
| IMAGE_IEF                             | image/ief                                      |
| IMAGE_WEBP                            | image/webp                                     |
| IMAGE_X_ICON                          | image/x-icon                                   |
| AUDIO_MIDI                            | audio/midi                                     |
| AUDIO_MPEG                            | audio/mpeg                                     |
| AUDIO_X_WAV                           | audio/x-wav                                    |
| AV                                    | audio/x-wav                                    |
| AUDIO_X_AIFF                          | audio/a-aiff                                   |
| AUDIO_WEBM                            | audio/webm                                     |
| AUDIO_OGG                             | audio/ogg                                      |
| AUDIO_WAV                             | audio/wav                                      |
| AUDIO_3GPP                            | audio/3gpp                                     |
| AUDIO_3GPP2                           | audio/3gpp2                                    |
| AUDIO_AAC                             | audio/aac                                      |
| AUDIO_AC3                             | audio/ac3                                      |
| AUDIO_AMR                             | audio/AMR                                      |
| AUDIO_AMR_WB                          | audio/AMR-WB                                   |
| AUDIO_AMR_WB_PLUS                     | audio/amr-wb+                                  |
| AUDIO_MP4                             | audio/mp4                                      |
| AUDIO_MP3                             | audio/mp3                                      |
| AUDIO_MP2                             | audio/mp2                                      |
| AUDIO_BASIC                           | audio/basic                                    |
| AUDIO_X_WMA                           | audio/x-ms-wma                                 |
| VIDEO_FLV                             | video/x-flv                                    |
| VIDEO_MPEG                            | video/mpeg                                     |
| VIDEO_PARITYFEC                       | video/parityfec                                |
| VIDEO_QUICKTIME                       | video/quicktime                                |
| VIDEO_X_MSVIDEO                       | video/x-msvideo                                |
| VIDEO_MP4                             | video/mp4                                      |
| VIDEO_X_FLV                           | video/x-flv                                    |
| VIDEO_OGG                             | video/ogg                                      |
| VIDEO_WEBM                            | video/webm                                     |
| VIDEO_3GPP                            | video/3gpp                                     |
| VIDEO_3GPP2                           | video/3gpp2                                    |
| VIDEO_RAW                             | video/raw                                      |
| VIDEO_X_WMV                           | video/x-ms-wmv                                 |
| VIEDO_X_M4V                           | video/x-m4v                                    |
| APPLICATION_MSWORD                    | application/msword                             |
| APPLICATION_RTF                       | application/rtf                                |
| APPLICATION_EXCEL                     | application/vnd.ms-excel                       |
| APPLICATION_JSON                      | application/json                               |
| APPLICATION_JSON_UTF8                 | application/json; charset=UTF-8                |
| APPLICATION_POWER_POINT               | application/vnd.ms-powerpoint                  |
| APPLICATION_JAVASCRIPT                | application/javascript                         |
| APPLICATION_OPEN_DOCUMENT_TEXT        | application/vnd.oasis.opendocument.text        |
| APPLICATION_OPEN_DOCUMENT_SPREADSHEET | application/vnd.oasis.opendocument.spreadsheet |
| APPLICATION_SHOCKWAVE_FLASH           | application/x-shockwave-flash                  |
| APPLICATION_RAR_COMPRESSED            | application/x-rar-compressed                   |
| APPLICATION_MS_DOWNLOAD               | application/x-msdownload                       |
| APPLICATION_CAB_COMPRESSED            | application/vnd.ms-cab-compressed              |
| APPLICATION_POSTSCRIPT                | application/postscript                         |
| APPLICATION_WWW_FORM_URLENCODED       | application/x-www-form-urlencoded              |
| APPLICATION_FONT_WOFF                 | application/x-font-woff                        |
| APPLICATION_FONT_TTF                  | application/octet-stream                       |
| APPLICATION_OCTET_STREAM              | application/octet-stream                       |
| APPLICATION_PDF                       | application/pdf                                |
| MULTIPART_ALTERNATIVE                 | multipart/alternative                          |
| MULTIPART_FORM_DATA                   | multipart/form-data                            |
| MULTIPART_BYTERANGES                  | multipart/byteranges                           |
| MULTIPART_DIGEST                      | multipart/digest                               |
| MULTIPART_ENCRYTED                    | multipart/encrypted                            |
| MULTIPART_HEADER_SET                  | multipart/header-set                           |
| MULTIPART_MIXED                       | multipart/mixed                                |
| MULTIPART_PARALLEL                    | multipart/parallel                             |
| MULTIPART_RELATED                     | multipart/related                              |
| MULTIPART_REPORT                      | multipart/report                               |
| MULTIPART_SIGNED                      | multipart/signed                               |
| MULTIPART_VOICE_MESSAGE               | multipart/vocie-message                        |
| UNKNOWN                               | UNKNOWN                                        |

Note the fields TEXT_PLAIN_UTF8, TEXT_HTML_UTF8, and APPLICATION_JSON_UTF8. In these fields, we added the corresponding charset type to the MIME type. These fields are generally used to return to the user, explicitly specifying the encoding parsing method for the user to parse.

At the end of the field, there is an UNKNOWN field. This field is added by the framework to mark a placeholder. For example, if a MIME type is not determined initially, it can be marked with the UNKNOWN field. Later, the type can be assigned a value. Finally, the current MIME type is checked to see if it is UNKNOWN, and if so, a default value is assigned.

## Field Conversion

During actual processing, the framework needs to convert between fields and their corresponding strings. The IHttpMime.h file declares the following functions:

```cpp
namespace IHttpMimeUtil
{
    IStringView toString(IHttpMime);
    IHttpMime toMime(const QString&);
    IHttpMime toMime(const IString&);
}
```

As shown above, users can use `IHttpMimeUtil::toString` to convert a MIME field into the corresponding string view IStringView. Using IStringView here can better save memory and reduce string copying.

Users can also use `IHttpMimeUtil::toMime` to convert a string into an IHttpMime field type. If the string does not match any MIME field during the conversion process, it will return `IHttpMime::UNKNOWN`.

## SuffixMime

The IHttpMime module supports mapping file suffixes to MIME strings. The function definition for this mapping is as follows:

```cpp
namespace IHttpMimeUtil
{
    IStringView getSuffixMime(const IString& suffix);
}
```

By passing a suffix into `getSuffixMime`, users can find the corresponding MIME string.

### Predefined Suffix-Mime Mappings

The framework internally defines some suffix-to-MIME mappings, as shown below:

| **File Suffix** | **MIME Type**                        |
| ------------ | ----------------------------------- |
| txt          | IHttpMime::TEXT_PLAIN_UTF8          |
| xhtml        | IHttpMime::TEXT_HTML_UTF8           |
| html         | IHttpMime::TEXT_HTML_UTF8           |
| htm          | IHttpMime::TEXT_HTML_UTF8           |
| css          | IHttpMime::TEXT_CSS                 |
| xml          | IHttpMime::TEXT_XML                 |
| xql          | IHttpMime::TEXT_XML                 |
| xsd          | IHttpMime::TEXT_XML                 |
| xslt         | IHttpMime::TEXT_XML                 |
| cml          | IHttpMime::TEXT_XML                 |
| dcd          | IHttpMime::TEXT_XML                 |
| ent          | IHttpMime::TEXT_XML                 |
| mtx          | IHttpMime::TEXT_XML                 |
| rdf          | IHttpMime::TEXT_XML                 |
| tsd          | IHttpMime::TEXT_XML                 |
| wsdl         | IHttpMime::TEXT_XML                 |
| xsl          | IHttpMime::TEXT_XML                 |
| biz          | IHttpMime::TEXT_XML                 |
| vxml         | IHttpMime::TEXT_XML                 |
| vml          | IHttpMime::TEXT_XML                 |
| tld          | IHttpMime::TEXT_XML                 |
| math         | IHttpMime::TEXT_XML                 |
| png          | IHttpMime::IMAGE_PNG                |
| jpg          | IHttpMime::IMAGE_JPEG               |
| jpeg         | IHttpMime::IMAGE_JPEG               |
| jpe          | IHttpMime::IMAGE_JPEG               |
| jfif         | IHttpMime::IMAGE_JPEG               |
| bmp          | IHttpMime::IMAGE_BMP                |
| cgm          | IHttpMime::IMAGE_CGM                |
| ief          | IHttpMime::IMAGE_IEF                |
| tif          | IHttpMime::IMAGE_TIFF               |
| tiff         | IHttpMime::IMAGE_TIFF               |
| webp         | IHttpMime::IMAGE_WEBP               |
| ico          | IHttpMime::IMAGE_X_ICON             |
| svg          | IHttpMime::IMAGE_SVG_XML            |
| gif          | IHttpMime::IMAGE_GIF                |
| mpga         | IHttpMime::AUDIO_MPEG               |
| aac          | IHttpMime::AUDIO_AAC                |
| ac3          | IHttpMime::AUDIO_AC3                |
| amr          | IHttpMime::AUDIO_AMR                |
| ogg          | IHttpMime::AUDIO_OGG                |
| wav          | IHttpMime::AUDIO_WAV                |
| 3gpp         | IHttpMime::AUDIO_3GPP               |
| rmi          | IHttpMime::AUDIO_MIDI               |
| mid          | IHttpMime::AUDIO_MIDI               |
| midi         | IHttpMime::AUDIO_MIDI               |
| webm         | IHttpMime::AUDIO_WEBM               |
| 3gp2         | IHttpMime::AUDIO_3GPP2              |
| aif          | IHttpMime::AUDIO_X_AIFF             |
| aiff         | IHttpMime::AUDIO_X_AIFF             |
| aifc         | IHttpMime::AUDIO_X_AIFF             |
| au           | IHttpMime::AUDIO_BASIC              |
| snd          | IHttpMime::AUDIO_BASIC              |
| wax          | IHttpMime::AUDIO_X_WAV              |
| mp3          | IHttpMime::AUDIO_MP3                |
| mp2          | IHttpMime::AUDIO_MP2                |
| wma          | IHttpMime::AUDIO_X_WMA              |
| flv          | IHttpMime::VIDEO_FLV                |
| mp4          | IHttpMime::VIDEO_MP4                |
| mpg          | IHttpMime::VIDEO_MPEG               |
| mp2v         | IHttpMime::VIDEO_MPEG               |
| mpeg         | IHttpMime::VIDEO_MPEG               |
| mps          | IHttpMime::VIDEO_MPEG               |
| avi          | IHttpMime::VIDEO_X_MSVIDEO          |
| 3gp          | IHttpMime::VIDEO_3GPP               |
| m4v          | IHttpMime::VIEDO_X_M4V              |
| wmv          | IHttpMime::VIDEO_X_WMV              |
| webm         | IHttpMime::VIDEO_WEBM               |
| mov          | IHttpMime::VIDEO_QUICKTIME          |
| json         | IHttpMime::APPLICATION_JSON         |
| js           | IHttpMime::APPLICATION_JAVASCRIPT   |
| bin          | IHttpMime::APPLICATION_OCTET_STREAM |
| exe          | IHttpMime::APPLICATION_OCTET_STREAM |
| pdf          | IHttpMime::APPLICATION_PDF          |

In the above `getSuffixMime` query, if the suffix is defined in the table, the corresponding definition is used. If the suffix is not defined, the user-defined MIME type is used. If no custom definition exists, OCTET_STREAM byte stream information is returned.

### User-Defined Suffix-Mime Mappings

If developers use suffixes not defined in the above predefined list, they can extend their own suffix mappings by inheriting the `IHttpRegistMimeInterface` class. Here is an example:

```cpp
// YkyMimeTask.h
#pragma once

#include "http/biscuits/IHttpRegistMimeInterface.h"

class YkyMimeTask : public IHttpRegistMimeInterface<YkyMimeTask>
{
public:
    YkyMimeTask() = default;

public:
    virtual QMap<IString, IString> mimes() const {
        return {
            {"yky", "application/yky"}
        };
    }
};

// YkyMimeTask.cpp
#include "YkyMimeTask.h"
``` 

In the above example, the yky suffix is registered to the system, mapping to the MIME type `application/yky`.