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
            url_env, execution_key, search_field,
            nested_field=None):
        self.session = requests.Session()
        self.formula_id = formula_id
        self.session.headers['Authorization'] = auth_header
        self.session.headers['Accept'] = "application/json"
        self.sales_orders = []
        self.step_name = step_name
        self.url_env = url_env
        self.execution_key = execution_key.format(
            step_name=self.step_name)
        self.field = search_field
        self.nested_field = nested_field
        self.execution_ids = None

    def get_formula_executions(self):
        self.executions = self.session.get(url=url.format(
            formula_id=self.formula_id, url_env=self.url_env)).json()
        self.execution_ids = [x['id'] for x in self.executions]

    def get_formula_execution(self, execution_id):
        steps = self.session.get(
            url=steps_url.format(
                execution_id=execution_id, url_env=self.url_env)).json()
        for step in steps:
            step['execution_values'] = self.session.get(
                url=step_execution_url.format(
                    step_execution_id=step['id'],
                    url_env=self.url_env)).json()
        return steps

    def step_through_execution(self, formula_execution_json):
        for i in formula_execution_json:
            print json.dumps(i, indent=2)
            yield

    def get_sales_orders(self, search_value=None, exit_when_found=False):
        self.sales_orders = []
        if not execution_ids:
            self.get_formula_executions()
        for execution_id in self.execution_ids:
            steps = self.session.get(
                url=steps_url.format(
                    execution_id=execution_id, url_env=self.url_env))
            step_ids = [
                x['id']
                for x in steps.json()
                if x['stepName'] == self.step_name]
            if len(step_ids) > 0:
                for step_id in step_ids:
                    step_values = self.session.get(
                        url=step_execution_url.format(
                            step_execution_id=step_id,
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
                            if self.nested_field is not None:
                                step_json = step_json[self.nested_field]
                            if self.field in step_json.keys():
                                if search_value is None or search_value == step_json[self.field]:
                                    self.sales_orders.append(
                                        (execution_id, step_json[self.field]))
                                    print "Found Sales Order {name} in {execution}".format(
                                        name=step_json[self.field],
                                        execution=execution_id,
                                        field=self.field)
                                    if exit_when_found:
                                        return
                            else:
                                print "'{field}' not found in {execution}!".format(
                                    execution=execution_id,
                                    field=self.field)
                                print json.dumps(step_json, indent=2)
                        else:
                            print "Didn't find {name} in Execution: {execution} Step: {step_id}".format(
                                name=self.step_name, execution=execution_id, step_id=step_id)
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
            url_env=env_string,
            execution_key="{step_name}.response.body",
            search_field='Other')

class ProdSalesOrder(PassTimeSalesOrder):
    def __init__(self):
        formula_id = 1474
        user_secret = "gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q="
        org_secret = "89341d5d002f3091e5cd5876d7ed8ff0"
        auth_header = "User {user}, Organization {org}".format(
            user=user_secret, org=org_secret)
        step_name = "salesorderLoop"
        env_string = "console"
        super(ProdSalesOrder, self).__init__(
            formula_id=formula_id,
            auth_header=auth_header,
            step_name=step_name,
            url_env=env_string,
            execution_key="{step_name}.entry",
            search_field='name',
            nested_field='attributes')
