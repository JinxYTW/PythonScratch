class IPManager:
    _instance = None

    def __init__(self):
        self.ip_addresses = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = IPManager()
        return cls._instance

    def set_ip_addresses(self, ip_addresses):
        self.ip_addresses = ip_addresses

    def add_ip_address(self, ip_address):
        self.ip_addresses.append(ip_address)

    def get_ip_addresses(self):
        return self.ip_addresses
    
    def get_ip_address1(self):
        return self.ip_addresses[0]
    
    def get_ip_address2(self):
        return self.ip_addresses[1]

