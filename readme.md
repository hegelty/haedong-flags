# haedong-flags
2023년 19기 해동 신입생 선발

# Docs
## login
* Method: GET
* endpoint: /login
* parameters:

|name|type|description|
|:---:|:---:|:---:|
|code|string|GBSWiki Oauth code|
* response:
  * success:  
```json
{
  "success": true,
  "session": "session id"
}
```
  * authorization failure:  
```json
{
  "success": false,
  "error": 1,
  "session": "session id"
}
```
  * not registered:  
```json
{
  "success": false,
  "error": 2,
  "session": "session id"
}
```
## register
* Method: POST
* cookies: session_id
* endpoint: /login/register
* from datas:

| name |type| description  |
|:----:|:---:|:------------:|
| name |string| student name |
| student_id | string | student id |

* response:
  * success:  
```json
{
  "success": true
}
```
  * error:  
```json
{
  "success": false,
  "error": 1
}
```
| error code | description |
|:----------:|:-----------:|
| 10 | name format error |
| 11 | student id format error |
| 20 | already registered |

## submit(normal problem)
* Method: POST
* cookies: session_id
* endpoint: /submit/<int:id>
* from datas:

| name |type| description  |
|:----:|:---:|:------------:|
| flag |string| flag |

* response:
  * success:  
```json
{
  "success": true
}
```
  * error:  
```json
{
  "success": false,
  "error": 1
}
```
| error code |                 description                 |
|:----------:|:-------------------------------------------:|
| 1 | already solved/not solved previous problems |
| 2 | wrong flag |

## submit(oobal problem)
* Method: POST
* cookies: session_id
* endpoint: /oobal/<int:id>
* from datas:

| name |type| description  |
|:----:|:---:|:------------:|
| flag |string| flag |

* response:
  * success:  
```json
{
  "success": true
}
```
  * error:  
```json
{
  "success": false,
  "error": 1
}
```
| error code |                 description                 |
|:----------:|:-------------------------------------------:|
| 1 | already solved |
| 2 | wrong flag |

## scoreboard
* Method: GET
* cookies: session_id(optional)
* endpoint: /scoreboard/api
* response:
  * success(not logged in):  
```json
[
  [
    "name",
    "student_id",
    "score(int)",
    "solved(int)"
  ]
]
```
  * success(logged in):  
```json
[
  [
    "name",
    "student_id",
    "score(int)",
    "solved(int)",
    [
      "solved oobal problem num(int)",
    ]
  ]
]
```