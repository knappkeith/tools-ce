import requests
import json

base_url = "https://{url_env}.cloud-elements.com" + \
    "/elements/api-v2/formulas/instances"
url = "%s/{formula_id}/executions" % base_url
step_execution_url = "%s/executions/steps/{step_execution_id}/values" % base_url
steps_url = "%s/executions/{execution_id}/steps" % base_url


class PassTimeSalesOrder(object):
    def __init__(
            self, formula_id,
            auth_header, step_name,
            url_env):
        self.session = requests.Session()
        self.formula_id = formula_id
        self.session.headers['Authorization'] = auth_header
        self.session.headers['Accept'] = "application/json"
        self.sales_orders = []
        self.step_name = step_name
        self.url_env = url_env
        self.execution_key = "{step_name}.response.body".format(
            step_name=self.step_name)
        self.field = 'Other'

    def get_formula_exections(self):
        self.executions = self.session.get(url=url.format(
            formula_id=self.formula_id, url_env=self.url_env)).json()
        self.execution_ids = [x['id'] for x in self.executions]

    def get_sales_orders(self):
        self.sales_orders = []
        for execution_id in self.execution_ids:
            steps = self.session.get(
                url=steps_url.format(
                    execution_id=execution_id, url_env=self.url_env))
            step_ids = [
                x['id']
                for x in steps.json()
                if x['stepName'] == self.step_name]
            if len(step_ids) > 0:
                step_values = self.session.get(
                    url=step_execution_url.format(
                        step_execution_id=step_ids[0],
                        url_env=self.url_env))
                if step_values > 0:
                    step_value = [
                        x['value']
                        for x in step_values.json()
                        if x['key'] == self.execution_key.format(
                            step_name=self.step_name)]
                    if len(step_value) > 0:
                        step_json = json.loads([
                            x['value']
                            for x in step_values.json()
                            if x['key'] == self.execution_key.format(
                                step_name=self.step_name)][0])
                        if self.field in step_json.keys():
                            self.sales_orders.append(
                                (execution_id, step_json[self.field]))
                            print "Found Sales Order {name} in {execution}".format(
                                name=step_json[self.field],
                                execution=execution_id,
                                field=self.field)
                        else:
                            print "'{field}' not found in {execution}!".format(
                                execution=execution_id,
                                field=self.field)
                    else:
                        print "Didn't find {name} in {execution}".format(
                            name=self.step_name, execution=execution_id)
                else:
                    print "Execution {name} doens't have steps?".format(
                        name=execution_id)
            else:
                print "Didn't find {name} in {execution}".format(
                    name=self.step_name, execution=execution_id)


class ProdUpdateRep(PassTimeSalesOrder):
    def __init__(self):
        formula_id = 2210
        user_secret = "gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q="
        org_secret = "89341d5d002f3091e5cd5876d7ed8ff0"
        auth_header = "User {user}, Organization {org}".format(
            user=user_secret, org=org_secret)
        step_name = "get-qbd-invoice"
        env_string = "console"
        super(ProdUpdateRep, self).__init__(
            formula_id=formula_id,
            auth_header=auth_header,
            step_name=step_name,
            url_env=env_string)
