async def main():
    # Configure logging only for standalone execution
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s",
        handlers=[logging.StreamHandler()],
    )

    config = get_settings_for_env()
    secret = get_token_from_idps(
        True,
        config.app_secret_path,
        config.idps_url,
        config.idps_policy,
        config.asset_id,
    )
    identity_connector = IdentityConnector(
        config.asset_alias,
        secret,
        config.app_job_id,
        config.identity_url,
        local=True,
    )
    slack_token = get_token_from_idps(
        config.local,
        config.slack_token_path,
        config.idps_url,
        config.idps_policy,
        config.asset_id,
    )
    enterprise_id = get_token_from_idps(
        config.local,
        config.slack_enterprise_id_path,
        config.idps_url,
        config.idps_policy,
        config.asset_id,
    )
    workspace_id = get_token_from_idps(
        config.local,
        config.slack_workspace_id_path,
        config.idps_url,
        config.idps_policy,
        config.asset_id,
    )

    ips_client = IPSBulkEntityClient(
        ips_base_url=config.ips_base_url,
        identity_connector=identity_connector,
    )

    slack_connector = SlackConnector(
        slack_api_base_url=config.slack_api_base_url,
        slack_token=slack_token,
        workspace_id=workspace_id,
        enterprise_id=enterprise_id,
    )
    dwm_connector = DWMProfileConnector(config.dwm_base_url, identity_connector)
    slack_member_fetcher = ParallelSlackMemberFetcher(
        slack_token, config.slack_api_base_url, workspace_id
    )
    await calculate_and_save_top_influencer_for_enterprise(
        slack_connector, dwm_connector, ips_client, slack_member_fetcher
    )
    await calculate_channel_importance_score_from_cache(dwm_connector, ips_client)


if __name__ == "__main__":
    asyncio.run(main())
