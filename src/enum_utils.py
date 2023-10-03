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


def wf_stage_descr(val: int) -> str:
    return _array_str(val, _WF_STAGES)


def _array_str(val: int, array: list, divisor: int = 10) -> str:
    if val == 0:
        return array[val]
    return array[int(val / divisor)]


def wf_can_generate_report(wf: int) -> bool:
    if wf == 0:
        return False

    step = int(wf / 10)
    return step >= 4 and step != len(_WF_STAGES) - 1


def result_bundle_type(val: int) -> str:
    return _array_str(val, _RB_TYPES)


def wf_progress_pct(wf: int) -> int:
    if wf == 0:
        return 0

    step = wf / 10
    if step >= 12:  # cancel
        return 0

    if step <= 2:  # order create / barcode
        return 5
    if step == 3:  # repeat
        return 15
    if step in [4, 5]:  # result / HL7
        return 25
    if step == 6:  # verify
        return 50
    if step == 7:  # final
        return 75
    if step > 7:  # collate / dispatch / fulfiled
        return 100

    return 0
