def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    log.info('database initialized')