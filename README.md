# crs-engine
💪 Crawler Script(CRS) engine (WIP)

## CRS
CRS(CRawling Script) is excute via this engine (written by Python)

CRS is named by me (ext: .crs)

- Example
```
SET TIMEOUT 5
SET DELAY 5
SET LOGLEVEL "DEBUG"
SET LOGPATH "./test.log"

PAGE "https://naver.com"
EL "a.link_login" @CLICK
EL "input#id" @INPUT("test")
EL "input#ps" @INPUT("1234")
EL "input#log.login" @CLICK

$NEWS = ELS "#NM_NEWSSTAND_DEFAULT_THUMB .thumb_box img"
LOOP NEWS
  $alt = ATR:alt
  
  IF $alt = "YTN"
    PRINT "THIS IS " + $alt
  ELSE
    PRINT $alt
  END
END
```

### SPEC
- SET: Global Setting
- PAGE: Load target URL
- EL: Find element
- ELS: Find elements (Array)
- ATR: Get attribute value
- ${NAME}: Variable
- IF/ELSE/END: If condition
- LOOP/END: Loop iterable or condition
- DOWNLOAD: Download resource (eg. image, html)
- @{ACTION}: Click, Touch, Input, ...
