import argparse

from data_model.transformer import Transformer
from data_model.nace import NACECODE
import constants as ct


def setup_args():
    parser = argparse.ArgumentParser(description='get nacecode')
    parser.add_argument('-i', '--company_ids', default=[""], type=str, nargs='+')

    return parser


def infer_nacecode(id_dscp: dict[str, str]) -> dict[str, str]:
    inferencer = Transformer()
    res = {}
    for id, dscp in id_dscp.items():
        try:
            inf = inferencer.query_nacecode(dscp)
            if inf:
                res[id] = res
        except Exception as e:
            print(f"error in querying hugging face: {e}")
    return res
    # return {id: inferencer.query_nacecode(dscp) for id, dscp in id_dscp.items()}


def run(query_ids: list[int]):
    my_nace = NACECODE(graph_url=ct.NACE_URL, auth_user=ct.NACE_USER, auth_pwd=ct.NACE_PWD,
                       node_label=ct.NACE_COMP_LABEL, node_dscp=ct.NACE_COMP_DSCP, nace_label=ct.NACE_CLASS_LABEL,
                       inf_key=ct.INF_LABEL, nace_rel=ct.NACE_REL, nace_pred_label=ct.NACE_PRED_LABEL)
    # step 1. get descripton. in: company_id: int(?), out: description: str
    id_dscp: dict[str: str] = my_nace.query_dscp(query_ids)

    # step 2. query nacecode. in: description: str, in: str, out:[int]
    id_code: dict[str: list[dict[str]]] = infer_nacecode(id_dscp)

    keys = list(id_dscp.keys())
    vals = [[{"label": "1520", "score": 0.77}, {"label": "3092", "score": 0.17}],
            [{"label": "1624", "score": 0.87}, {"label": "3101", "score": 0.09}]]
    id_code = dict(zip(keys, vals))

    # step 3. populate back into db NACEGroup<->PortofolioCompany ?. in: [id:int, [nacecode:int], rel: str] 49.4->49.04?
    del id_dscp
    my_nace.update_nacecode(id_code_dict=id_code)


if __name__ == '__main__':
    parser = setup_args()
    query_ids: list[str] = parser.parse_args().company_ids
    if query_ids:
        run(query_ids=query_ids)


# async, sinks in between steps
# edge cases
#