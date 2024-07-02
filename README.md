# cf-dyndns

A Cloudflare dynamic DNS client.

## Installation

```bash
git clone https://github.com/rael-san/cf-dyndns
cd cf-dyndns
pip install .
```

## Usage

Create a config file:

```yaml
CF_API_TOKEN: <cloudflare-api-token>
ZONE_ID: <zone-id>
RECORD_NAME: <record-name> (e.g. www.example.com)
```

Getting a zone ID:

```bash
curl -s https://api.cloudflare.com/client/v4/zones \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json"
```

Running cf-dyndns:

```bash
cf-dyndns --config <path-to-config.yml>
```

### Docker

A docker image is packaged with the repository.

```bash
docker pull ghcr.io/rael-san/cf-dyndns
```

The docker image expects a config file named `config.yml` in a `/configs`
directory. Use a volume mount to add this file to the container:

```bash
docker run -d -t -v /path/to/config/dir:/configs ghcr.io/rael-san/cf-dyndns
```

## License

MIT
