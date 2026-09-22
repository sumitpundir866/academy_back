# user login api 
            # screen_ids = (
            #     db.query(RoleScreenMap.screen_id)
            #     .filter(RoleScreenMap.role_id == role.role_id)
            #     .all()
            # )

            # screen_ids = [s.screen_id for s in screen_ids]

            # screens = (
            #     db.query(Screens)
            #     .filter(Screens.id.in_(screen_ids))
            #     .all()
            # )

            # screen_list = [
            #     {
            #         "screen_id": s.id,
            #         "screen_name": s.screen_name,
            #         "screen_url": s.screen_url,
            #         "screen_type":s.sc_type,
            #         "module_id": s.module_id
            #     }
            #     for s in screens
            # ]

            # module_ids = list({s.module_id for s in screens})

            # modules = (
            #     db.query(ModuleMaster)
            #     .filter(ModuleMaster.id.in_(module_ids))
            #     .all()
            # )

            # module_list = [
            #     {
            #         "module_id": m.id,
            #         "module_name": m.module_name,
            #         "module_url": m.module_url
            #     }
            #     for m in modules
            # ]