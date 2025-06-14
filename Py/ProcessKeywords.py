import json
from collections import defaultdict

DATAPATH = 'Data/'

def dump_set(set_name, file_name):
    file_name += ".json"
    json_ready = {k: list(v) for k, v in set_name.items()}
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(json_ready, f, ensure_ascii = False, indent=4)

#fields
fields = defaultdict(set)
fields = {}
fields['ai'] = {
    "ai", "artificial intelligence", "machine learning", "deep learning", 
    "ml", "nlp", "computer vision", "neural network", "chatbot", 
    "data science", "data scientist", "tensorflow", "pytorch", "model training",
    "trí tuệ nhân tạo", "nhân tạo"
}
fields['data'] = {
    "data", "data analyst", "data analysis", "data mining", "data visualization", 
    "tableau", "excel", "pandas", "sql", "data warehouse", "etl", 
    "analytics", "insights", "data modeling", "data storytelling", "dashboard",
    "kpi", "bi tools", "business intelligence", "data lake", "big data", "snowflake",
    "redshift", "phân tích dữ liệu", "trí tuệ dữ liệu", "cơ sở dữ liệu", "database",
    "quản trị dữ liệu", "infra", "bi", "powerbi", "power bi"
}
fields['software'] = {
    "software", "developer", "lập trình", "dev", "devops",
    "php", "java", "python", "c", "c++", "golang", "ruby", "nodejs", "nestjs",
    "dotnet", ".net", "backend", "backend developer", "back-end", "back end",
    "back-end dev", "be dev", "server-side", "api developer", "restful api", 
    "graphql", "microservices", "service architecture", "software engineer",
    "fullstack", "mobile", "ios", "android", "ứng dụng", "phần mềm",
    "software developer", "software architect"
}
fields['web'] = {
    "frontend", "frontend developer", "front-end", "front end", "front-end dev", 
    "fe dev", "ui developer", "frontend engineer", "fe engineer", "user interface dev", 
    "responsive design", "html", "css", "sass", "less", "tailwind", "bootstrap", 
    "material ui", "mui", "cross-browser", "web components", "react", "reactjs", 
    "react developer", "vuejs", "vue developer", "svelte", "angular", 
    "web", "website", "web developer", "web designer", "webflow", "wordpress", 
    "shopify", "magento", "wix", "cms", "content management system", "ui", "ux"
}
fields['cloud'] = {
    "cloud", "azure", "aws", "gcp", "cloud engineer", "cloud devops", "cloud-native",
    "cloud ops", "ci/cd", "pipeline", "build automation", "infrastructure as code",
    "terraform", "ansible", "helm", "kubernetes", "docker", "gitlab ci", "github actions",
    "site reliability engineer", "sre", "monitoring", "logging", "prometheus", "grafana"
}
fields['hardware'] = {
    "hardware", "it support", "desktop support", "helpdesk", "it technician", 
    "kỹ thuật máy tính", "phần cứng", "bios", "motherboard", "ram", "cpu", "gpu"
}
fields['system'] = {
    "system", "system admin", "sysadmin", "linux admin", "windows server", 
    "active directory", "virtualization", "vmware", "hyper-v", "nagios", "zabbix", 
    "prometheus", "ansible", "scripting", "bash", "powershell", "shell",
    "system architecture", "it operations", "incident management", "operation",
    "quản trị hệ thống", "hệ thống", "server management", "uptime", "capacity planning", 
    "configuration management", "linux kernel", "kernel engineer", "linux kernel developer",
    "system engineer", "powerapps", "erp", "information system"
}
fields['network'] = {
    "network engineer", "network administrator", "network architect", 
    "network operations", "network specialist", "network infrastructure", 
    "network security", "network monitoring", "packet capture", "wireshark",
    "network troubleshooting", "ccna", "ccnp", "cisco", "router", "switch", 
    "firewall", "load balancer", "vpn", "dns", "dhcp", "mpls", "bgp", "ospf", 
    "lan", "wan", "voip", "quản trị mạng", "hệ thống mạng", "linux engineer",
    "network", "kỹ thuật mạng"
}
fields['security'] = {
    "cybersecurity", "information security", "infosec", "application security", 
    "endpoint security", "penetration testing", "pentest", "ethical hacking", 
    "red team", "blue team", "threat detection", "vulnerability", "firewall", 
    "ids", "ips", "siem", "security analyst", "security engineer", 
    "incident response", "risk management", "zero trust", "iso 27001", "nist", 
    "soc", "data protection", "access control", "identity management", "iam", 
    "detection and response", "malware", "encryption", "phishing", "compliance", 
    "gdpr", "bảo mật", "an ninh mạng", "an toàn thông tin", "server engineer",
    "pentester"
}
fields['bridge'] = {
    "brse", "bridge engineer", "bridge system engineer", "onsite coordinator", 
    "jp-vi bridge", "client communication", "cầu nối", "bridge", "comtor"
}
fields['embedded_iot'] = {
    "iot", "embedded", "firmware development", "microcontroller", 
    "raspberry pi", "arduino", "real-time", "rtos", "sensor", "actuator", 
    "nhúng", "robotics"
}
fields['business'] = {
    "ba", "business analyst", "business",
    "phân tích nghiệp vụ", "stakeholder", "secretary",
    "kế toán", "quản trị rủi ro", "hr", "nhân sự", "hcns",
    "internal auditor", "pr", "public relations", "strategic planner"
}
fields['marketing'] = {
    "marketing", "digital marketing", "performance marketing", "seo", "content", 
    "social media", "campaign", "brand", "copywriting", "email marketing", "google adwords"
}
fields['qa_qc'] = {
    "qa", "qa engineer", "qc", "qc engineer", "test engineer", 
    "manual testing", "automation testing", "unit testing", "integration testing", 
    "test case", "test plan", "bug tracking", "defect management", 
    "selenium", "jmeter", "postman", "api testing", 
    "kiểm thử", "kỹ sư kiểm thử", "quality assurance", "tester"
}
fields['blockchain'] = {
    "blockchain", "smart contract", "smartcontract", "solidity", "web3", 
    "web3 developer"
}
fields['ecommerce'] = {
    "ecommerce", "e-commerce", "online shopping", "retail tech", 
    "order management", "payment gateway", "checkout", 
    "shopping cart", "product catalog", "flash sale", 
    "logistics tech", "inventory system", "thương mại điện tử"
}
fields['bank'] = {
    "bank", "banking", "finance", "financial", "fintech", 
    "core banking", "digital banking", "payment system", 
    "credit", "loan", "pos", "ngân hàng", "tài chính", "b2b"
}
fields['tech_management'] = {
    "project manager", "product manager", "scrum master", "product owner", 
    "technical manager", "project leader", "tech-lead", "tech lead", "lead engineer", 
    "solution architect", "project coordinator", "quản lý dự án", "delivery manager",
    "technical lead", "technical leader", "chief technology officer", "iteration manager"
}
fields['management'] = {
    "quản lý nhà máy", "kiểm soát quy trình", "quản lý chất lượng"
}
fields['installation'] = {
    "lắp đặt", "cài đặt", "thi công",
    "technician",
}
fields['game'] = {
    "game developer", "game designer", "game programmer", 
    "unity", "unreal", "unreal engine", "godot", "cocos", 
    "game engine", "gamedev", "phát triển game", "lập trình game",
    "game artist", "2d", "3d", "game", "playable ads"
}
fields['media'] = {
    "graphic designer", "multimedia designer", "visual designer",
    "creative designer", "visuals", "design", "figma", "sketch", "adobe xd", 
    "photoshop", "illustrator", "indesign", "after effects", "invision", "canva", "storyboard", 
    "thiết kế đồ họa", "video editor", "video", "designer", "livestream", "live stream"
}
fields['tech_support'] = {
    "máy in", "điện thoại", "sửa chữa", "bảo hành", "camera",
    "máy móc", "máy tính", "tech support", "technical support",
    "hỗ trợ kỹ thuật", "hỗ trợ kĩ thuật", "nhân viên kỹ thuật",
    "nhân viên kĩ thuật", "dịch vụ kỹ thuật"
}
fields['r&d'] = {
    "r&d", "nghiên cứu"
}
fields['service'] = {
    "service desk", "hỗ trợ khách hàng", "lễ tân", "chăm sóc khách hàng",
    "chuyên viên khách hàng", "cskh"
}
fields['engineer'] = {
    "cad", "wpf", "cae", "fpga"
}
fields['mechanic'] = {
    "operations engineer", "ép kính"
}
fields['it'] = {
    'it', 'cntt', 'công nghệ thông tin', "công nghệ"
}
# fields['unclassified'] = {
#     "nhân viên vận hành", "nhân viên kĩ thuật", "nhân viên", 
#     "kỹ thuật viên", "chuyên viên", "giáo viên", "lễ tân"
# }
dump_set(fields, DATAPATH + "fields_archive")

#currency
currency = defaultdict(set)
currency = {}
currency["DEAL"] = {
    "deal", "negotiate", "negotiating", "negotiation", "negotiable",
    "thoa thuan", "thoả thuận", "thỏa thuận", "thuong luong", "thương lượng"
}
currency["VND"] = {
    "vnd", "việt", "nam", "đ", "dong", "đồng", "chuc", "chục", "trăm",
    "nghin", "nghìn", "ngàn", "ngan", "tr", "trieu", "triệu"
}
currency["USD"] = {
    "usd", "$", "us$", "dollar", "dollars",
    "hundred", "thousand", "million", "mil"
}
dump_set(currency, DATAPATH + "currency_archive")

#unit
unit = defaultdict(set)
unit = {}
unit["10"] = {"chục", "chuc"}
unit["100"] = {"trăm", "hundred"}
unit["1000"] = {"nghin", "nghìn", "ngàn", "ngan", "k", "thousand"}
unit["1000000"] = {"tr", "trieu", "triệu", "m", "million", "mil"}
dump_set(unit, DATAPATH + "unit_archive")

#experience
experiences = defaultdict(set)
experiences = {}
experiences['manager_leader'] = {
    "manager", "leader", 
    "lead", "head of", "trưởng", "quản lý", 
    "giám đốc", "điều phối", "owner"
}
experiences['senior'] = {
    "senior", "sr", "cao cấp", "cấp cao", 
}
experiences['middle'] = {
    "middle", "mid", "mid level", "chuyên viên",
    "kỹ sư", "engineer"
}
experiences['junior'] = {
    "junior", "jr", "nhân viên"
}
experiences['fresher'] = {
    "fresher", "new grad", "ra trường", 
    "entry level",
}
experiences['intern'] = {
    "intern", "internship", "thực tập", 
    "học việc", "trainee"
}
dump_set(experiences, DATAPATH + "experiences_archive")