import json
import requests

def check_http_health(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status_code": response.status_code,
            "status": "success" if response.ok else "fail"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "status": "error",
            "error": str(e)
        }

def montar_url(service):
    try:
        host = service["host"]
        port = service["port"]
        endpoint = service["health_endpoint"]
        return f"http://{host}:{port}{endpoint}"
    except KeyError as e:
        raise KeyError(f"Chave ausente no serviço: {e}")

def main():
    try:
        with open("input.json") as f:
            services = json.load(f)
    except FileNotFoundError:
        print("Arquivo 'input.json' não encontrado.")
        return

    results = []

    for service in services:
        name = service.get("name", "Serviço sem nome")
        print(f"\nINFO: Verificando serviço: {name}")

        try:
            url = montar_url(service)
            result = {
                "name": name,
                "url": url,
                "port_check": check_http_health(url)
            }
        except KeyError as e:
            result = {
                "name": name,
                "url": None,
                "port_check": {
                    "status": "error",
                    "error": str(e)
                }
            }

        results.append(result)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()