import json,sys
e=json.load(sys.stdin)
print("equipo",e.get("nombre"),"| nivel",e["nivel_actual"],"| aprobados",e["niveles_aprobados"],"| puede_enviar",e["puede_enviar"],"| reenviar_en",e.get("puede_reenviar_en"),"| corte",e["corte_equipo"],"| repo",e.get("repo"))
for h in e["historial"][-3:]:
    r=h.get("resultado") or {}
    print("- N%s %s %s %s %s  %s"%(h["nivel"],h["commit"][:7],h["estado"],r.get("veredicto"),r.get("puntaje"),h.get("mensaje")))
    for f in r.get("faltantes",[]): print("   *",f)
