from sqlalchemy_pos_declarative import PositionEntity


def updateNewPositionEntity(session, exec_data_dict):
    autotrader_id = exec_data_dict['autotrader_id']
    shortcd = exec_data_dict['shortcd']
    # print exec_data_dict
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

        # print 'new position'
        # print new_positionentity.holdqty
        # print new_positionentity.buysell
        # print new_positionentity.avgexecprice
        session.add(new_positionentity)
    elif len(rows) == 1:
        old_PositionEntity = rows[0]
        print (exec_data_dict['shortcd'],
               old_PositionEntity.holdqty,
               old_PositionEntity.buysell,
               old_PositionEntity.avgexecprice,
               )
        print exec_data_dict['execprice'] * exec_data_dict['execqty'], exec_data_dict['execqty']

        old_PositionEntity.datetime = exec_data_dict['datetime']
        if old_PositionEntity.buysell == exec_data_dict['buysell']:
            old_PositionEntity.avgexecprice = (exec_data_dict['execprice'] * exec_data_dict['execqty'] +
                                              old_PositionEntity.avgexecprice * old_PositionEntity.holdqty) / \
                                              (old_PositionEntity.holdqty + exec_data_dict['execqty'])
            old_PositionEntity += exec_data_dict['execqty']
        elif old_PositionEntity.holdqty == 0:
            old_PositionEntity.holdqty = exec_data_dict['execqty']
            old_PositionEntity.buysell = exec_data_dict['buysell']
            old_PositionEntity.avgexecprice = exec_data_dict['execprice']
        else:
            if old_PositionEntity.holdqty == exec_data_dict['execqty']:
                session.delete(old_PositionEntity)
            elif old_PositionEntity.holdqty < exec_data_dict['execqty']:
                old_PositionEntity.avgexecprice = exec_data_dict['execprice']
                old_PositionEntity.buysell = exec_data_dict['buysell']
                old_PositionEntity.holdqty = abs(int(exec_data_dict['execqty']) - old_PositionEntity.holdqty)
            elif old_PositionEntity.holdqty > int(exec_data_dict['execqty']):
                old_PositionEntity.holdqty -= int(exec_data_dict['execqty'])

    session.commit()
    pass
