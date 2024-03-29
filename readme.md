# haedong-flags
2023년 19기 해동 신입생 선발

# Docs
* General errors
* 
```json
{
  "success": false,
  "error": 1
}
```
| error code |   description   |
|:----------:|:---------------:|
| 0 | unknown error |
|     -1     |  require login  |
|     -2     | session expired |

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
| 2 | already registered |

## submit
* Method: POST
* cookies: session_id
* endpoint: /submit
* from datas:

| name |type| description  |
|:----:|:---:|:------------:|
| flag |string| flag |

* response:
  * success:
```json
{
  "success": true,
  "oobal": true/false
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

## scoreboard
* Method: GET
* cookies: session_id(optional)
* endpoint: /scoreboard/api
* response:
  * success:  
```json
{
  "success": true,
  "login": true/false,
  "oobal": true/false,
  "oobal_len": "oobal problem length(int)",
  "problem_len": "problem length(int)",
  "data": [
    {
      "name": "name",
      "student_id": "student id",
      "score": "score(int)",
      "solved": [
        True/False,
      ]
    }
  ]
}
```

## user info
* Method: GET/POST
* cookies: session_id
* endpoint: /user/info
* response:
  * success:  
```json
{
  "id": "user id",
  "success": true,
  "name": "name",
  "student_id": "student id",
  "score": "score(int)",
  "oobal": true/false,
  "oobal_len": "oobal problem length(int)",
  "problem_len": "problem length(int)"
  "solved": [
    True/False,
  ]
}
```

## user oobal info
* Method: GET/POST
* cookies: session_id
* endpoint: /user/oobal
* response: 1 if solved, 0 if not solved
