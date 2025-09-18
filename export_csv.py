import geoip2.database
import ipaddress
import csv

# Load ASN database
reader = geoip2.database.Reader("GeoLite2-ASN.mmdb")
country_reader = geoip2.database.Reader("GeoLite2-Country.mmdb")

seen = set()
with open("vietnam_isps.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ASN", "ISP"])
    
    # Dải IP IPv4 public toàn cầu
    for net in ipaddress.ip_network("0.0.0.0/0").subnets(new_prefix=8):
        try:
            # Lấy quốc gia
            c = country_reader.country(str(net.network_address))
            if c.country.iso_code != "VN":
                continue

            # Lấy ASN
            asn = reader.asn(str(net.network_address))
            key = (asn.autonomous_system_number, asn.autonomous_system_organization)
            if key not in seen:
                seen.add(key)
                writer.writerow(key)
        except Exception:
            continue

print("Done. Xuất ra vietnam_isps.csv")
