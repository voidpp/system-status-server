About
-

This is a very lightweight stuff to get some system status info in JSON.

Available nodes:
-

- Uptime
- Load
- CPU (number of cores)
- Memory usage

Dependencies:
-

- psutil

Typical out:
-
```json
{
	"load": [0.29, 0.33, 0.27],
	"uptime": 3403979,
	"cpu": {
		"cores": 8
	},
	"memory": {
		"available": 13979320320,
		"total": 16503238656,
		"percent": 15.3,
		"free": 2553470976,
		"used": 13949767680
	}
}
```
