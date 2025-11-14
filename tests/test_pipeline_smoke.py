from src.run_eval import main

def test_run_eval_smoke(tmp_path, monkeypatch):
    # run into temp outputs
    monkeypatch.chdir(tmp_path)
    main(out_jsonl="out.jsonl", out_csv="out.csv", top_k=3)
    assert (tmp_path / "out.jsonl").exists()
    assert (tmp_path / "out.csv").exists()
