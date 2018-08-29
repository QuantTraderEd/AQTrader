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
        old_position_entity = rows[0]
        print ('old_position',
               exec_data_dict['shortcd'],
               old_position_entity.holdqty,
               old_position_entity.buysell,
               old_position_entity.avgexecprice,
               )

        old_position_entity.datetime = exec_data_dict['datetime']
        if old_position_entity.buysell == exec_data_dict['buysell']:
            old_position_entity.avgexecprice = (exec_data_dict['execprice'] * exec_data_dict['execqty'] +
                                              old_position_entity.avgexecprice * old_position_entity.holdqty) / \
                                              (old_position_entity.holdqty + exec_data_dict['execqty'])
            old_position_entity.holdqty += exec_data_dict['execqty']
        elif old_position_entity.holdqty == 0:
            old_position_entity.holdqty = exec_data_dict['execqty']
            old_position_entity.buysell = exec_data_dict['buysell']
            old_position_entity.avgexecprice = exec_data_dict['execprice']
        else:
            if old_position_entity.holdqty == exec_data_dict['execqty']:
                session.delete(old_position_entity)
            elif old_position_entity.holdqty < exec_data_dict['execqty']:
                old_position_entity.avgexecprice = exec_data_dict['execprice']
                old_position_entity.buysell = exec_data_dict['buysell']
                old_position_entity.holdqty = abs(int(exec_data_dict['execqty']) - old_position_entity.holdqty)
            elif old_position_entity.holdqty > int(exec_data_dict['execqty']):
                old_position_entity.holdqty -= int(exec_data_dict['execqty'])

    session.commit()
    pass
