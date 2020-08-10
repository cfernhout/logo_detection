import requests

resp = requests.post(
    "http://localhost:5000/predict",
    files={
        "file": open(
            "/Users/jesse/projects/keurmerken-od/data/test/Topkeurmerken.jpg",
            "rb",
        )
    },
)
