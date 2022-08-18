import requests
# url = 'http://localhost:5000/api'
url = 'http://127.0.0.1:5000/api'
r = requests.post(url,json={
	"ssc_p": "50",
	"hsc_p": "50",
	"degree_p": "50",
	"etest_p": "50",
	"mba_p": "50",
	"gender": "0",
	"ssc_b": "0",
	"hsc_b": "0",
	"hsc_s": "0",
	"degree_t": "0",
	"workex": "0",
	"specialisation": "0"
})
print(r.json())