class Exchange:
    def truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier