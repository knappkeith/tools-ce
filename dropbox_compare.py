import requests


class CloudElementsElementRequest(requests.Session):
    def __init__(
            self,
            base_url,
            user_secret,
            org_secret,
            element_token,
            *args, **kwargs):
        
        super(CloudElementsElementRequest, self).__init__(*args, **kwargs)
        
        self.base_url = base_url
        self.history = []
        self.user_secret = user_secret
        self.org_secret = org_secret
        self.element_token = element_token
        self.headers['Accept'] = 'application/json'
        self.admin_auth = self._build_auth_header(user=user_secret, org=org_secret)
        self.element_auth = self._build_auth_header(user=user_secret, org=org_secret, token=element_token)
        self.headers['Authorization'] = self.element_auth

    def _build_auth_header(self, user, org, token=None):
        items = ["User {user}", "Organization {org}"]
        if token is not None:
            items.append("Element {element}".format(element=token))
        return ", ".join(items).format(user=user, org=org)


def compare_json(left, right, path="ROOT"):
    print ""
    if left == right:
        # print "good" 
        return True
    if type(left) == list:
        if len(left) > len(right):
            print "Unmatched length: {} > {}".format(len(left), len(right))
        if len(right) > len(left):
            print "Unmatched length: {} < {}".format(len(left), len(right))
        if isinstance(left[0], dict):
            sort_key = left[0].keys()[0]
            left_sorted = sorted(left, key=lambda x: x[sort_key])
            right_sorted = sorted(right, key=lambda x: x[sort_key])
        else:
            left_sorted = sorted(left)
            right_sorted = sorted(right)
    elif type(left) == dict:
        left_keys = sorted(left.keys())
        right_keys = sorted(right.keys())
        if left_keys != right_keys:
            print "Unmatched Keys:\n    {} !=\n    {}".format(sorted(left.keys()), sorted(right.keys()))
            if len(left_keys) != len(right_keys):
                if len(left_keys) > len(right_keys):
                    rm_keys = [x for x in left_keys if x not in right_keys]
                elif len(left_keys) < len(right_keys):
                    rm_keys = [x for x in right_keys if x not in left_keys]
                for rm_key in rm_keys:
                    print "    removing {}".format(rm_key)
                    try:
                        del left[rm_key]
                    except:
                        pass
                    try:
                        del right[rm_key]
                    except:
                        pass
        left_sorted = sorted(left.iteritems())
        right_sorted = sorted(right.iteritems())
    elif type(left) == str or type(left) == unicode:
        print "{}:\n    {} != {}".format(path, left, right)
        return
    else:
        print type(left)
        return 

    if left_sorted == right_sorted:
        # print "good" 
        return True

    for index in range(0, len(left_sorted)):
        if left_sorted[index] != right_sorted[index]:
            if isinstance(left_sorted[index], tuple):
                if isinstance(left_sorted[index][1], dict):
                    # print "dropping " + str(left_sorted[index][0]) 
                    compare_json(left_sorted[index][1], right_sorted[index][1], path="{}>{}".format(path, left_sorted[index][0]))
                elif  isinstance(left_sorted[index][1], list):
                    if index > len(left_sorted) or index > len(right_sorted):
                        pass
                    else:
                        compare_json(left_sorted[index][1], right_sorted[index][1], path="{}>{}".format(path, left_sorted[index][0]))
                else:
                    print "{}:\n    {} !=\n    {}".format("{}>{}".format(path, left_sorted[index][0]), left_sorted[index], right_sorted[index])
            else:
                # print "Dropping"
                compare_json(left_sorted[index], right_sorted[index], path="{}>{}".format(path, index))
        else:
            # print "good"
            pass

db_new = CloudElementsElementRequest(
    base_url="https://snapshot.cloud-elements.com/elements/api-v2/hubs/documents/{resource}",
    user_secret="wUA03uERFYxWMb+1E1ncNh0B9jEZJ8YOUlgJDOeFPrE=",
    org_secret="bc15df3fd4922fd66879960cd69539eb",
    element_token="ZMHeFOkEABYZ1HmmPPtyp8CRbPmbQCOyXF09scf5cRA=")
db_old = CloudElementsElementRequest(
    base_url="https://console.cloud-elements.com/elements/api-v2/hubs/documents/{resource}",
    user_secret="MaDbkG4uvwgD2zgPrdlnENXejNwBsbgpIbsbidxLm2E=",
    org_secret="fcf15248575c541a640a5828d77a6ae8",
    element_token="ZJEHPBLDNuAq2Dwh6VM/BM+QqXF/NaoN+s8Ptwai3NU=")