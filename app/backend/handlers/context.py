from backend.models import Building, Apartment, ConsumptionReport, Measurment


def get_user_context(month, season, owner_id):
    
    apartment = Apartment.objects.get(owner_id=owner_id)
        
    # get all apt reports  
    consumption_apartment_all = ConsumptionReport.objects.filter(apartment_id=apartment.id)
    
    # get combinations of season/month
    season_month_dict = consumption_apartment_all.values("month", "season").distinct().order_by("-month").all()
    
    # set first month of season if season provided
    if season:
        
        # get first month for season
        month = season_month_dict.filter(season=season)[0]["month"]
    
    # if month is not in request or season is not provided, get the latest month
    if not month:
        month = season_month_dict[0]["month"]
        season = season_month_dict[0]["season"]
    
    # try to get result or fail
    try:
        consumption_apartment = consumption_apartment_all.filter(month=month).first()
        consumption_building = ConsumptionReport.objects.filter(building_id = apartment.building.id, month=month, type="Building").first()
        measurments = Measurment.objects.filter(consumption_report_id=consumption_apartment.id)
    except ConsumptionReport.DoesNotExist:
        consumption_apartment = None
        consumption_building = None
        measurments = None
            
    return {
        "measurments": measurments,
        "apartment": apartment,
        "consumption_apartment": consumption_apartment,
        "consumption_building": consumption_building,
        "measurments": measurments,
        "season": season,
        "month": month,
        "season_month_dict": season_month_dict
    }