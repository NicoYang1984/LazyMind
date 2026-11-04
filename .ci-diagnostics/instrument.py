from pathlib import Path
import sys
root=Path(sys.argv[1]);kind=sys.argv[2]
if kind=='pg':
 p=root/'backend/core/workflow/external_agent_recovery_test.go';s=p.read_text();s=s.replace('if string(before) != string(after) {','if string(before) != string(after) {\n\t\tlogRecoverySnapshotDiff(t, before, after)');p.write_text(s)
 (p.parent/'external_agent_recovery_diagnostic_test.go').write_text('''package workflow
import("encoding/json";"fmt";"reflect";"sort";"testing")
func logRecoverySnapshotDiff(t *testing.T, before, after []byte) {
 t.Helper(); var a,b any; if err:=json.Unmarshal(before,&a);err!=nil {t.Fatal(err)};if err:=json.Unmarshal(after,&b);err!=nil {t.Fatal(err)}
 var walk func(string,any,any)
 walk=func(path string,a,b any){
  if reflect.DeepEqual(a,b){return}
  if am,ok:=a.(map[string]any);ok {if bm,ok:=b.(map[string]any);ok {keys:=map[string]bool{};for k:=range am{keys[k]=true};for k:=range bm{keys[k]=true};var names []string;for k:=range keys{names=append(names,k)};sort.Strings(names);for _,k:=range names{walk(path+"."+k,am[k],bm[k])};return}}
  if aa,ok:=a.([]any);ok {if bb,ok:=b.([]any);ok&&len(aa)==len(bb){for i:=range aa{walk(fmt.Sprintf("%s[%d]",path,i),aa[i],bb[i])};return}}
  t.Logf("[DIAG-pr921] field=%s before=%#v after=%#v",path,a,b)
 };walk("$",a,b)
}
''')
else:
 p=root/'local/lazymind-cli/internal/agentexec/desktop_query_windows_test.go';s=p.read_text();old='\tbody, err := command.Output()';new='''	started := time.Now()
	body, err := command.Output()
	var stderr []byte
	if exitErr, ok := err.(*exec.ExitError); ok { stderr = exitErr.Stderr }
	exitCode := -1
	if command.ProcessState != nil { exitCode = command.ProcessState.ExitCode() }
	t.Logf("[DIAG-pr921] elapsed=%s ctx=%v exit=%d error=%v stderr=%q stdout=%q", time.Since(started), ctx.Err(), exitCode, err, stderr, body)''';assert s.count(old)==1;p.write_text(s.replace(old,new))
