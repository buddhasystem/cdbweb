from .models		import *

class PayloadInformation:
    """
    Adapted (with changes) from b2s):
    A container class for efficient comparison between global tags"""
    
    def __init__(self, gtp):
        
        payload = Payload.objects.get(pk=gtp.payload_id)
        
        self.name = Basf2Module.objects.get(pk=payload.basf2_module_id).name
        self.checksum = payload.checksum
            
        iov = PayloadIov.objects.filter(global_tag_payload_id=gtp.global_tag_payload_id)[0]
        self.iov = iov.exp_start, iov.run_start, iov.exp_end, iov.run_end
        
    def __str__(self):
        stringifyIovs = ' '.join(map(str, self.iov))
        return self.name+' '+self.checksum+' '+stringifyIovs
        

    def __hash__(self):
        """Make object hashable"""
        return hash((self.name, self.checksum, self.iov))

    def __eq__(self, other):
        """Check if two payloads are equal"""
        return (self.name, self.checksum, self.iov) == (other.name, other.checksum, other.iov)

    def __lt__(self, other):
        """Sort payloads by name, iov, revision"""
        return (self.name.lower(), self.iov, self.rev) < (other.name.lower(), other.iov, other.rev)

    def readable_iov(self):
        """return a human readable name for the IoV"""
        if self.iov == (0, 0, -1, -1):
            return "always"

        e1, r1, e2, r2 = self.iov
        if e1 == e2:
            if r1 == 0 and r2 == -1:
                return "exp {e1}"
            elif r2 == -1:
                return "exp {e1}, runs {r1}+"
            elif r1 == r2:
                return "exp {e1}, run {r1}"
            else:
                return "exp {e1}, runs {r1} - {r2}"
        else:
            if r1 == 0 and r2 == -1:
                return "exp {e1}-{e2}, all runs"
            elif r2 == -1:
                return "exp {e1}, run {r1} - exp {e2}, all runs"
            else:
                return "exp {e1}, run {r1} - exp {e2}, run {r2}"

# Original:        
    # def __init__(self, payload, iov):
    #     """Set all internal members from the json information of the payload and the iov.

    #     Arguments:
    #         payload (dict): json information of the payload as returned by REST api
    #         iov (dict): json information of the iov as returned by REST api
    #     """
    #     #: name of the payload
    #     self.name = payload['basf2Module']['name']
    #     #: checksum of the payload
    #     self.checksum = payload['checksum']
    #     #: interval of validity
    #     self.iov = iov["expStart"], iov["runStart"], iov["expEnd"], iov["runEnd"]
    #     #: revision, not used for comparisons
    #     self.rev = payload["revision"]
    #     #: payload id in CDB, not used for comparisons
    #     self.payload_id = payload["payloadId"]
    #     #: iov id in CDB, not used for comparisons
    #     self.iov_id = iov["payloadIovId"]
