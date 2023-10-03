_WF_STAGES: list[str] = [
    "Unknown",
    "Order Created",
    "Specimen Label Print",
    "Repeat Procedure",
    "Resulted",
    "HL7 Imported",
    "Validated",
    "Finalized",
    "Collated",
    "Dispatched",
    "Remotely Dispatched",
    "Fulfilled",
    "Canceled",
]

_RB_TYPES = ["Unarchived", "Discrete", "Template", "UserTemplate"]


def workflow_stage_descr(val: int) -> str:
    return _array_str(val, _WF_STAGES)


def _array_str(val: int, array: list, divisor: int = 10) -> str:
    if val == 0:
        return array[val]
    return array[int(val / divisor)]


def wf_can_generate_report(val: int) -> bool:
    if val == 0:
        return False
    wf = int(val / 10)
    return wf >= 4 and wf != len(_WF_STAGES) - 1


def result_bundle_type(val: int) -> str:
    return _array_str(val, _RB_TYPES)
