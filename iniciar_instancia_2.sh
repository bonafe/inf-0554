#flavor: m1.tiny.cpu-shared
#Image: CentOS-7-x86_64
#Security Group: all-all
#Network: ip4 e ip6
openstack server create --flavor 9f4fea12-453d-4f04-9f34-08a6651e151b --image d787be84-ab4e-4061-8b1a-9104c6c58006 --security-group 03e9a3c7-ba8e-4b90-b8d1-09b7c784b5f2 --network ae068da4-6c83-4b73-9dc4-7ae84fdfa6b5 --user-data cloud.init --min 1 --max 1 eredes32_33_teste
