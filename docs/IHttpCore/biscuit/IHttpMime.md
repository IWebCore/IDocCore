 #  IHttpMime

## Mime 字段

在 IHttpCore 中，框架将一部分常用的 mime 类型定义成enum 字段。用户可以直接使用 字段的名称来代替mime 字符串。如下是预定义的字段和类型以及mime 的对应内容。

| ***字段***                            | ***MIME 类型***                                |
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

注意上面的 TEXT_PLAIN_UTF8， TEXT_HTML_UTF8， APPLICATION_JSON_UTF8 这三个字段，我们在 mime 类型的后面添加了对应的 charset 类型。这些字段一般用于返回给用户，明确指定用户的编码解析方式，便于用户解析。



在字段的最后有一个 UNKNOWN 字段。 这个字段是框架添加的字段，用于标记代替使用。比如如果一个mime 类型在内容还没有确定的时候，可以标记 UNKNOWN字段，在中间会给该类型赋值。在最后判断当前的mime 类型是否是 UNKNOWN，如果是的话，则给一个默认值。



## 字段转换

在实际的过程中，框架需要将字段和对应的字符串进行相互转换, 在 IHttpMime.h 文件中声明了如下的函数：

```
namespace IHttpMimeUtil
{
    IStringView toString(IHttpMime);
    IHttpMime toMime(const QString&);
    IHttpMime toMime(const IString&);
}
```

如上，用户可以使用 `IHttpMimeUtil::toString` 将一个 mime 字段转换成对弈的字符串视图 IStringView 。这里使用 IStringView可以更好的节省内存，减少字符串的拷贝。

用户也可以使用 `IHttpMimeUtil::toMime` 将一个字符串转换成 IHttpMime 字段类型。如果在实际的转换过程中，字符串并没有匹配到任何一个Mime字段，则会返回 `IHttpMime::UNKNOWN` 字段。



## SuffixMime

IHttpMime 模块支持文件尾缀 到 mime 字符串的映射。这个映射的函数定义如下：

```
namespace IHttpMimeUtil
{
    IStringView getSuffixMime(const IString& suffix);
}
```

通过 getSuffixMime 传入 suffix 来查找特定的mime字符串。



### 预定义的suffix-mime

框架内部预定义了一部分的suffix 和 mime 的映射关系， 如下：

| **‌文件后缀‌** | **MIME类型‌**                        |
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

在上述的`getSuffixMime` 的查询中，如果suffix 在上面的表格中有定义，则会使用表个中的定义，如果没有定义，则会使用用户自定义的 mime 类型，如果用户没有自定义，则会放回 OCTET_STREAM 的字节流的信息。



### 用户自定义 suffix-mime 映射

如果开发者使用了在上述预定义后缀之外的后缀，用户可以通过继承  `IHttpRegistMimeInterface` 类来扩展自己的 suffix 映射，下面举一个例子：

```c++
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

上述例子中将 yky 的后缀注册到系统中，yky 后缀映射到 `application/yky` 这个mime。