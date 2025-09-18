from flask import Flask, request, jsonify
import geoip2.database

# Đường dẫn DB (cập nhật bằng geoipupdate)
ASN_DB = "GeoLite2-ASN.mmdb"
CITY_DB = "GeoLite2-City.mmdb"

asn_reader = geoip2.database.Reader(ASN_DB)
city_reader = geoip2.database.Reader(CITY_DB)

app = Flask(__name__)

@app.route("/lookup")
def lookup():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing ip parameter"}), 400

    result = {"ip": ip}

    try:
        asn = asn_reader.asn(ip)
        result["asn"] = asn.autonomous_system_number
        result["isp"] = asn.autonomous_system_organization
    except Exception:
        result["asn"] = None
        result["isp"] = None

    try:
        city = city_reader.city(ip)
        result["country"] = city.country.name
        result["region"] = city.subdivisions.most_specific.name
        result["city"] = city.city.name
    except Exception:
        result["country"] = None
        result["region"] = None
        result["city"] = None

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
