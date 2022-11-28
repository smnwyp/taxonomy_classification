import py2neo

class NACECODE:
    def __init__(self, graph_url, auth_user: str, auth_pwd: str, node_label: str, node_dscp: str, nace_label: str,
                 inf_key: str, nace_rel: str, nace_pred_label:str):
        self.graph = self.start_db(graph_url=graph_url, auth_user=auth_user, auth_pwd=auth_pwd)
        self.node_label = node_label
        self.node_dscp = node_dscp
        self.nace_label = nace_label
        self.matcher = py2neo.NodeMatcher(self.graph)
        self.inf_key = inf_key
        self.nace_rel = nace_rel
        self.nace_pred_label = nace_pred_label

    def start_db(self, graph_url, auth_user: str, auth_pwd: str) -> py2neo.Graph:
        return py2neo.Graph(graph_url, auth=(auth_user, auth_pwd))

    def query_dscp(self, query_ids: [str]) -> dict[str: str]:
        # edge cases
        res = {id: list(self.matcher.match(self.node_label).where(slug=id))[0][self.node_dscp] for id in query_ids}
        return res

    @staticmethod
    def transform_hugging_nace_pred(nace: str) -> str:
        """
        quick hack
        Args:
            nace:

        Returns:

        """
        return nace[0]+nace[1]+'.'+nace[2]+nace[3]

    def update_nacecode(self, id_code_dict: dict[str: list[dict[str]]]):
        all_rel = []
        for company_id, nace_preds in id_code_dict.items():
            company_node = list(self.matcher.match(self.node_label).where(slug=company_id))[0]
            nace_nodes = [list(self.matcher.match(self.nace_label)
                               .where(full_numeric_code=NACECODE.transform_hugging_nace_pred(pred[self.inf_key])))[0]
                          for pred in nace_preds]
            all_rel = all_rel + [py2neo.Relationship(company_node, self.nace_rel, nace_node) for nace_node in list(nace_nodes)]
        for rel in all_rel:
            self.graph.create(rel)

    def helper_get_ids(self):
        return [i["slug"] for i in list(self.matcher.match(self.node_label))]

    def verify(self, id_code_dict: dict[int: list[str]]) -> bool:
        verification = False
        return verification