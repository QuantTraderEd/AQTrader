from sqlalchemy_pos_declarative import PositionEntity


def insertNewPositionEntity(session, position_info_dict):
    autotrader_id = position_info_dict['autotrader_id']
    shortcd=position_info_dict['shortcd']
    rows = session.query(PositionEntity).filter(PositionEntity.autotrader_id == autotrader_id)\
                                        .filter(PositionEntity.shortcd == shortcd).all()
    if len(rows) == 0:
        new_positionentity = PositionEntity(autotrader_id=position_info_dict['autotrader_id'],
                                            datetime=position_info_dict['datetime'],
                                            shortcd=position_info_dict['shortcd'],
                                            buysell=position_info_dict['buysell'],
                                            avgexecprice=position_info_dict['avgexecprice'],
                                            holdqty=position_info_dict['holdqty'],
                                            )
        session.add(new_positionentity)
    elif len(rows) == 1:
        old_PositionEntity = rows[0]
        old_PositionEntity.datetime = position_info_dict['datetime']
        old_PositionEntity.buysell = position_info_dict['buysell']
        old_PositionEntity.avgexecprice = position_info_dict['avgexecprice']
        old_PositionEntity.holdqty = position_info_dict['holdqty']

    session.commit()
    pass

if __name__ == '__main__':
    import datetime as dt
    import sqlalchemy_pos_init as pos_init

    session = pos_init.initSession('autotrader_position.db')

    position_info_dict = dict()
    position_info_dict['autotrader_id'] = 'OTM001'
    position_info_dict['datetime'] = dt.datetime.strptime('2017-07-17 09:10:03.456506', '%Y-%m-%d %H:%M:%S.%f')
    position_info_dict['buysell'] = 'sell'
    position_info_dict['shortcd'] = '301M9270'
    position_info_dict['avgexecprice'] = 0.11
    position_info_dict['holdqty'] = 4

    insertNewPositionEntity(session, position_info_dict)

    rs = session.query(PositionEntity).all()

    for positionentity in rs:
        print (positionentity.autotrader_id, positionentity.shortcd,
               positionentity.avgexecprice, positionentity.buysell, positionentity.holdqty,
               positionentity.datetime)
        if positionentity.holdqty == 0:
            session.delete(positionentity)

    session.commit()
    rows = session.query(PositionEntity.shortcd).all()
    print list(zip(*rows)[0])