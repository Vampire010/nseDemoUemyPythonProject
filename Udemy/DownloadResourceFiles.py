import requests
import json

url = "https://www.udemy.com/api-2.0/ecl?client_key=js&client_version=0e6e05e"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "text/plain",
    "dwn-profiling": "Cg1Bc2lhL0NhbGN1dHRhEMoCGMoCIgtHb29nbGUgSW5jLigIOMAMQIQHSgVXaW4zMlIGeDg2XzY0WgVlbi1HQmIFZW4tR0JiBWVuLUlOYgVlbi1VU2ICZW5qBmNocm9tZXABehBSEP/mGSYBCrcxZCAe/eJSggEQ4M1cXagHG8mKUxX+RjFHCogBGJgBAaABAKgBALABALgBDMABAMgBANABANgBAOABAfgBAYACAYgCAJACEpoCEFVPNApns9U0kH9cZRfnTfClAgBQFUOtAgBQFUO1AgBQFUO9AgAEEEPFAgAI80LNAgCAFUHVAgDcE0PaAhDAXiArdH9UcFAzqZFC/Y5s4AIA6AL88/////////8B8AIy+AKEDIADAZIDEKFZ2bTrmWp7mrF87BjeqB6YAwWiAxDBQrN5ygGO9Za6Ttivx59LqgNRQU5HTEUgKEFNRCwgQU1EIFJhZGVvbihUTSkgR3JhcGhpY3MgKDB4MDAwMDE2NEMpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpsgMRR29vZ2xlIEluYy4gKEFNRCnAAwHIA8/p2uaJM9ADiqvt5okz2AOHjojAiDPiA3xNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUV4cXJ3RlVpNDZKOVIxNTN0VG5sQnBrVWVVR3dEc0crVmNWT01RQlpWdEptMldZTkFnVTBtN3pJdlNzbldMTDVyb1FaV1JvcVB3RlFzazhmNGRGd05EUT096gNgTUVVQ0lIRjlmL0pUWCtHWGR4MERMQzZHYy9oZXlGM2toUStxbEw1MXFWN1FtRVo3QWlFQXhOS2ljWFF1cjA5SVZETkNOZ3hYZGNLQmRFS0toY1dtTGttVUgyVkJlc0U9igQgOGE1NzkwMTY1MzE3NGQyZjliNTgxOTAwZDAwMjk5MDiaBLwCCBoQmN0QGCkgBEIgCAEVAABAQB1aa69EJQV/lkMt1kMRQzUXzB1DPbqCvENCIAgCFb0bD0AdLXZQRCVW+1xDLcra5EI1a1f3Qj2CGHhDQiAIAxUAADBBHQCglkQlAAB/Qy0AAMRCNQAA+UI9WSiLQ0IgCAQV89gKPR1ddCFBJckMsD8tW3srPzXDUYE/PYyd3T9CIAgFFQAAAAAd128FPyWvUdY9LSvzxDw1K/PEPD3XmBU+QiAIBhUAAAAAHQAAgD8lDM7HPC0AAAAANQAAAAA9qvUdPkIgCAcVAAAAAB0AAMBCJc+FqEAtAACAPzUAAIBAPfHN0EBCIAgIFQAAsEEdAAAAQiUAANhBLQAAIEE1AAAAQj0AAKBAQiAICRUAALhCHQAAC0MlAAD7Qi0AAABANQCAB0M9ZS2bQaoEBAgCEALCBCA2OTAyZGM2NDM2ZDU0N2Y3YmU4NDMxOGJmMGMzYzliOMoEB2luZGV4RELSBAVFQ0RTQdoEDlNFQ1VSRV9JRF9TRU5U4gQHV2luZG93c+oEAjEx8gQGQ2hyb21l+gQDMTM4igUgZGYyZTgyM2YxMWJhNDMwNDk0N2RlZDZjMDc1NDAwNzSSBR4VAADwQR0AAHRCJQAAaEItAAAAADUAAHBCPUDA70CaBQx2MS41LjIxLTE4MDWqBSAQsJWXjQEY8L21QCDhqNvmiTMoiavt5okzMPy83OaJM8IFBAECLgPKBQEB0AUC2AXP6drmiTPgBYqr7eaJM4oGDTIwMi42Mi45My4xNjmaBhoIh3IQzLmZj9MDGO/1u1Eg6+6rRyiAgPD/D6gGAA==",
    "origin": "https://www.udemy.com",
    "priority": "u=1, i",
    "referer": "https://www.udemy.com/course/learn-selenium-automation-in-easy-python-language/learn/lecture/2505942",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

cookies = {
    "__udmy_2_v57r": "b8723d948ca74f7a8deedd62a352f378",
    "ud_firstvisit": "2025-08-08T04:47:58.440390+00:00:1ukF1K:wA-fLyw8v12kZ_bY2cwzsoFEyapbTmmvi-0cIqigGEk",
    # ... add rest of cookies here in the same key-value style ...
}

payload = [
    {
        "eventType": "CourseTakingContentDownloadEvent",
        "eventData": {
            "createTime": 1754978274805,
            "sendTime": 1754978276743,
            "eventId": "NGY4NTMwN2YtYWVjYS00YW",
            "_type": "CourseTakingContentDownloadEvent",
            "clientHeader": {
                "appKey": "web_main",
                "sourceServiceName": "website-django",
                "organizationId": None,
                "userId": 256172910,
                "visitorUuid": "b8723d948ca74f7a8deedd62a352f378",
                "sessionId": "ZWViZjk3ZTAtYzgxYy00Ym",
                "clientId": "YTA1YjUyODAtMTMwNy00Nj",
                "page": {
                    "trackingId": "MDU5MjI1OTUtNTJmOC00ZT",
                    "key": "course_taking_curriculum_item"
                },
                "isMobile": False,
                "isD2CSubscriber": False
            },
            "courseTakingHeader": {
                "courseId": 397068,
                "userMode": "student"
            },
            "resourceType": "file_download",
            "curriculum": {
                "curriculumType": "lecture",
                "curriculumId": 2505942,
                "practiceSubType": None
            }
        }
    }
]

response = requests.post(url, headers=headers, cookies=cookies, json=payload)
print(response.status_code, response.text)