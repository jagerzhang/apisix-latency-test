curl -X PUT -d@upstream.json http://127.0.0.1:9080/apisix/admin/upstreams/test -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
curl -X PUT -d@service.json http://127.0.0.1:9080/apisix/admin/services/test -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
curl -X PUT -d@route.json http://127.0.0.1:9080/apisix/admin/routes/test -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
