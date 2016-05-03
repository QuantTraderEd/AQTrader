from sqlalchemy_pos_declarative import PositionEntity


def updateNewPositionEntity(session, exec_data_dict):
    autotrader_id = exec_data_dict['autotrader_id']
    shortcd = exec_data_dict['shortcd']
    rows = session.query(PositionEntity).filter(PositionEntity.autotrader_id == autotrader_id)\
                                        .filter(PositionEntity.shortcd == shortcd).all()
    if len(rows) == 0:
        new_positionentity = PositionEntity(autotrader_id=exec_data_dict['autotrader_id'],
                                            datetime=exec_data_dict['datetime'],
                                            shortcd=exec_data_dict['shortcd'],
                                            buysell=exec_data_dict['buysell'],
                                            avgexecprice=exec_data_dict['execprice'],
                                            holdqty=exec_data_dict['execqty'],
                                            )
        session.add(new_positionentity)
    elif len(rows) == 1:
        old_PositionEntity = rows[0]
        old_PositionEntity.datetime = exec_data_dict['datetime']
        if old_PositionEntity.buysell == exec_data_dict['buysell']:
            old_PositionEntity.holdqty += exec_data_dict['execqty']
            old_PositionEntity.avgexecprice = (exec_data_dict['execprice'] * exec_data_dict['execqty'] +
                                              old_PositionEntity.avgexecprice * old_PositionEntity.holdqty) / \
                                              (old_PositionEntity.holdqty)
        else:
            old_PositionEntity.holdqty -= exec_data_dict['execqty']
            if old_PositionEntity.holdqty == 0:
                del old_PositionEntity
            else:
                old_PositionEntity.holdqty = abs(old_PositionEntity.holdqty)
                old_PositionEntity.avgexecprice = exec_data_dict['execprice']
                old_PositionEntity.buysell = exec_data_dict['buysell']

    session.commit()
    pass
